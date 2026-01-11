import boto3

ec2 = boto3.client("ec2")
cw = boto3.client("cloudwatch")

# ===== CONFIG =====
WARNING_CPU = 50
CRITICAL_CPU = 80

WARNING_MEMORY = 50
CRITICAL_MEMORY = 80

WARNING_DISK = 30
CRITICAL_DISK = 10

SNS_WARNING = "arn:aws:sns:ap-northeast-1:051820856223:saisos-prd-warning"
SNS_CRITICAL = "arn:aws:sns:ap-northeast-1:051820856223:saisos-prd-critical"

# ==================

def build_alarm_name(ec2_name, metric, level):
    return f"ec2_{ec2_name}_{metric}_{level}"

def put_alarm(
    name,
    description,
    namespace,
    metric,
    dimensions,
    threshold,
    sns_topic,
    operator="GreaterThanOrEqualToThreshold",
):
    cw.put_metric_alarm(
        AlarmName=name,
        AlarmDescription=description,
        Namespace=namespace,
        MetricName=metric,
        Dimensions=dimensions,
        Statistic="Average",
        Period=300,
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=threshold,
        ComparisonOperator=operator,
        TreatMissingData="notBreaching",
        AlarmActions=[sns_topic],
    )

def put_disk_free_alarm(
    name,
    description,
    instance_id,
    threshold,
    sns_topic,
):
    cw.put_metric_alarm(
        AlarmName=name,
        AlarmDescription=description,
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=threshold,
        ComparisonOperator="LessThanOrEqualToThreshold",
        TreatMissingData="notBreaching",
        AlarmActions=[sns_topic],
        Metrics=[
            {
                "Id": "diskfree",
                "Label": "DiskFreePercent",
                "ReturnData": False,
                "MetricStat": {
                    "Metric": {
                        "Namespace": "CWAgent",
                        "MetricName": "disk_free_percent",
                        "Dimensions": [
                            {"Name": "InstanceId", "Value": instance_id}
                        ],
                    },
                    "Period": 300,
                    "Stat": "Average",
                },
            },
            {
                "Id": "minDiskFree",
                "Label": "MinDiskFreePercent",
                "Expression": "MIN(METRICS())",
                "ReturnData": True,
            },
        ],
    )

def delete_alarms(names):
    if names:
        cw.delete_alarms(AlarmNames=names)

def get_tag(tags, key):
    for t in tags:
        if t["Key"] == key:
            return t["Value"]
    return "unknown"

def lambda_handler(event, context):
    instance_id = event["detail"]["instance-id"]
    state = event["detail"]["state"]

    # Get tags of EC2
    res = ec2.describe_instances(InstanceIds=[instance_id])
    instance = res["Reservations"][0]["Instances"][0]
    tags = instance.get("Tags", [])

    ec2_name = get_tag(tags, "Name")
    monitor  = get_tag(tags, "Monitor")

    if monitor.lower() != "true":
        return

    # Delete alarms when EC2 stopped/terminated
    if state in ["stopped", "terminated"]:
        alarm_names = [
            build_alarm_name(ec2_name, "CPU", "warning"),
            build_alarm_name(ec2_name, "CPU", "critical"),
            build_alarm_name(ec2_name, "Memory", "warning"),
            build_alarm_name(ec2_name, "Memory", "critical"),
            build_alarm_name(ec2_name, "Disk", "warning"),
            build_alarm_name(ec2_name, "Disk", "critical"),
        ]   
        delete_alarms(alarm_names)
        return

    # Create alarms when EC2 started
    if state != "running":
        return

    # CPU
    put_alarm(
        build_alarm_name(ec2_name, "CPU", "warning"),
        f"AWS 【システム】 {ec2_name}　サーバで　CPU >= 50%の問題が発生しました。",
        "AWS/EC2",
        "CPUUtilization",
        [{"Name": "InstanceId", "Value": instance_id}],
        WARNING_CPU,
        SNS_WARNING,
    )

    put_alarm(
        build_alarm_name(ec2_name, "CPU", "critical"),
        f"AWS 【システム】 {ec2_name}　サーバで　CPU >= 80%の問題が発生しました。",
        "AWS/EC2",
        "CPUUtilization",
        [{"Name": "InstanceId", "Value": instance_id}],
        CRITICAL_CPU,
        SNS_CRITICAL,
    )

    # Memory
    put_alarm(
        build_alarm_name(ec2_name, "Memory", "warning"),
        f"AWS 【システム】 {ec2_name}　サーバで　Memory >= 50%の問題が発生しました。",
        "CWAgent",
        "mem_used_percent",
        [{"Name": "InstanceId", "Value": instance_id}],
        WARNING_MEMORY,
        SNS_WARNING,
    )

    put_alarm(
        build_alarm_name(ec2_name, "Memory", "critical"),
        f"AWS 【システム】 {ec2_name}　サーバで　Memory >= 80%の問題が発生しました。",
        "CWAgent",
        "mem_used_percent",
        [{"Name": "InstanceId", "Value": instance_id}],
        CRITICAL_MEMORY,
        SNS_CRITICAL,
    )

    # Disk (/)
    put_disk_free_alarm(
        build_alarm_name(ec2_name, "Disk", "warning"),
        f"AWS 【システム】 {ec2_name}　サーバで　Disk <= 30%の問題が発生しました。",
        instance_id,
        WARNING_DISK,
        SNS_WARNING,
    )
    put_disk_free_alarm(
        build_alarm_name(ec2_name, "Disk", "critical"),
        f"AWS 【システム】 {ec2_name}　サーバで　Disk <= 10%の問題が発生しました。",
        instance_id,
        CRITICAL_DISK,
        SNS_CRITICAL,
    )
