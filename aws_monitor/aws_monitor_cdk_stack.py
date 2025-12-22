from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from .constructs.log_groups import LogGroups

class AwsMonitorCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, *, configs: dict | None = None, **kwargs) -> None:
        """AwsMonitorCdkStack

        Args:
            scope: Construct scope
            construct_id: id
            configs: optional mapping of config file stems to parsed YAML content
                Example keys: 'log_groups', 'systems'
        """
        super().__init__(scope, construct_id, **kwargs)

        # store configs for later use
        self.configs = configs or {}

        # If configs provide 'log_groups' (list of group names) and 'systems'
        # (mapping env -> system -> list of resources), create LogGroups for
        # each env/system using the configured groups.
        logs = self.configs.get("logs")
        systems = self.configs.get("systems")

        #Get project name for prefix
        project_prefix = self.node.try_get_context("project") or "AwsMonitor"

        if logs and systems:
            # logs may be a mapping or a list; support both shapes
            # if isinstance(logs, dict) and "log_groups" in logs:
            #     groups = logs["log_groups"]
            # else:
            #     groups = logs if isinstance(logs, list) else []

            for env_name, systems_map in systems.items():
                if not isinstance(systems_map, dict):
                    continue

                if isinstance(logs, dict):
                    groups = logs.get("log_groups", [])
                else:
                    groups = logs

                for system_name in systems_map.keys():
                    # create a LogGroups construct per env/system
                    LogGroups(
                        self,
                        f"LogGroups-{env_name}-{system_name}",
                        env=env_name,
                        system=system_name,
                        groups=groups,
                        prefix = project_prefix
                    )
                    

