import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_monitor.aws_monitor_cdk_stack import AwsMonitorCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_monitor_cdk/aws_monitor_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsMonitorCdkStack(app, "aws-monitor-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
