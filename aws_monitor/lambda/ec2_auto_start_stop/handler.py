import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client("ec2")

TAG_KEY = "AutoStartStop"
TAG_VALUE = "true"


def get_instances():
    response = ec2.describe_instances(
        Filters=[
            {
                "Name": f"tag:{TAG_KEY}",
                "Values": [TAG_VALUE]
            },
            {
                "Name": "instance-state-name",
                "Values": ["running", "stopped"]
            }
        ]
    )

    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(instance["InstanceId"])

    return instances


def lambda_handler(event, context):
    action = event.get("action")
    if action not in ["start", "stop"]:
        raise ValueError("Invalid action")

    instances = get_instances()

    if not instances:
        logger.info("No instances found")
        return

    if action == "start":
        ec2.start_instances(InstanceIds=instances)
        logger.info(f"Started instances: {instances}")

    elif action == "stop":
        ec2.stop_instances(InstanceIds=instances)
        logger.info(f"Stopped instances: {instances}")

