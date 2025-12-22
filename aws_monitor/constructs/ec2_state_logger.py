from constructs import Construct
from aws_cdk import (
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_logs as logs,
    Duration,
)

class Ec2StateLoggerConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        prefix: str,
    ):
        super().__init__(scope, id)

        fn = _lambda.Function(
            self,
            f"{prefix}-Ec2StateLoggerFn",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda/ec2_state_logger"),
            timeout=Duration.seconds(30)
        )

        fn.add_to_role_policy(
            iam.PolicyStatement(
                f"{prefix}-Ec2StateLoggerPolicy",
                policy_name=f"{prefix}-Ec2StateLoggerPolicy",
                statements=[
                    iam.PolicyStatement(
                        sid="WriteEc2StateLogs",
                        actions=[
                            "logs:CreateLogStream",
                            "logs:PutLogEvents"
                        ],
                        resources=["*"]
                    ),
                    iam.PolicyStatement(
                        sid="DescribeEc2",
                        actions=["ec2:DescribeInstances"],
                        resources=["*"]
                    )
                ]
            )
        )

        rule = events.Rule(
            self,
            f"{prefix}-Ec2StateChangeRule",
            event_pattern=events.EventPattern(
                source=["aws.ec2"],
                detail_type=["EC2 Instance State-change Notification"],
                detail={
                    "state": ["running", "stopped"]
                }
            )
        )

        rule.add_target(targets.LambdaFunction(fn))
