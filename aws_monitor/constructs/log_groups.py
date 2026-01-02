from typing import Iterable, Dict

from aws_cdk import RemovalPolicy
from aws_cdk import aws_logs as logs
from typing import Iterable, Dict
import re

from aws_cdk import RemovalPolicy
from aws_cdk import aws_logs as logs
from constructs import Construct


class LogGroups(Construct):
    """Construct that creates multiple CloudWatch Log Groups.

    Each log group name will follow the pattern:
        /<env>/<system>/state
        /<env>/<system>/resource
        /<env>/<system>/service
        /<env>/<system>/application

    Example:
        LogGroups(self, "LGs", env="prod", system="payment")
        -> creates `/prod/payment/resource/ap_memory` and `/prod/payment/resource/db_memory`
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        env: str,
        system: str,
        groups: Iterable[str], # e.g. ['state', 'resource', 'service', 'application']
        prefix: str, # project prefix
        retention: logs.RetentionDays = logs.RetentionDays.ONE_YEAR,
        removal_policy: RemovalPolicy = RemovalPolicy.DESTROY,
    ) -> None:
        super().__init__(scope, id)

        if not env or not system:
            raise ValueError("Both `env` and `system` must be provided and non-empty")

        self.env = env
        self.system = system
        self.groups = list(groups)
        self.retention = retention
        self.removal_policy = removal_policy

        # Created LogGroup objects by resource name
        self.log_groups: Dict[str, logs.LogGroup] = {}

        self._create_log_groups()

    def _to_camel(self, s: str) -> str:
        """Convert an arbitrary string into deterministic CamelCase for logical IDs.

        Non-alphanumeric characters are treated as separators. Empty parts are dropped.
        Examples: 'prod' -> 'Prod', 'staging-us' -> 'StagingUs'
        """
        parts = re.split(r"[^0-9a-zA-Z]+", s)
        return "".join(p.capitalize() for p in parts if p)

    def _create_log_groups(self) -> None:
        for group in self.groups:
            # CloudWatch log group name
            name = f"/{self.env}/{self.system}/{group}"

            # Deterministic logical id that includes env and system so it's unique
            logical_id = (
                f"{self._to_camel(self.env)}{self._to_camel(self.system)}{self._to_camel(group)}"
            )

            # Create log group
            lg = logs.LogGroup(
                self,
                logical_id,
                log_group_name=name,
                retention=self.retention,
                removal_policy=self.removal_policy,
            )

            self.log_groups[name] = lg

    def get_log_group(self, resource: str) -> logs.LogGroup:
        """Return the created `LogGroup` for `resource` (e.g. 'ap' or 'db')."""
        return self.log_groups[resource]
