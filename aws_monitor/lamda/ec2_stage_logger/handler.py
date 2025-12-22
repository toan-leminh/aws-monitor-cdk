import boto3
import time
import json

ec2 = boto3.client("ec2")
logs = boto3.client("logs")

def get_tag(tags, key):
    for t in tags:
        if t["Key"] == key:
            return t["Value"]
    return "unknown"

def handler(event, context):
    instance_id = event["detail"]["instance-id"]
    state = event["detail"]["state"]  # running | stopped

    res = ec2.describe_instances(InstanceIds=[instance_id])
    instance = res["Reservations"][0]["Instances"][0]
    tags = instance.get("Tags", [])

    name = get_tag(tags, "Name")
    env = get_tag(tags, "Env")
    system = get_tag(tags, "System")

    log_group = f"{env}/{system}/state"
    log_stream = name

    timestamp = int(time.time() * 1000)
    message = json.dumps({
        "instance_id": instance_id,
        "state": state,
        "name": name
    })

    # Create log stream if not exists
    try:
        logs.create_log_stream(
            logGroupName=log_group,
            logStreamName=log_stream
        )
    except logs.exceptions.ResourceAlreadyExistsException:
        pass

    logs.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[
            {
                "timestamp": timestamp,
                "message": message
            }
        ]
    )
