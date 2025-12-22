#!/usr/bin/env python3
import os
import aws_cdk as cdk
from pathlib import Path
import yaml

from typing import Any, Dict
from aws_monitor.aws_monitor_cdk_stack import AwsMonitorCdkStack


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def load_all_yaml_configs(config_dir: Path) -> Dict[str, Any]:
    """Load all .yml/.yaml files from `config_dir` and return a mapping
    from filename stem to parsed content.
    Example: config/log_groups.yaml -> {"log_groups": [...]}
    """
    configs: Dict[str, Any] = {}
    if not config_dir.exists():
        return configs

    # collect both .yml and .yaml files in sorted order for determinism
    paths = sorted(config_dir.glob("*.yml")) + sorted(config_dir.glob("*.yaml"))
    for p in paths:
        configs[p.stem] = load_yaml(p)

    return configs


# Read configurations from YAML files in config/
root = Path(__file__).resolve().parent
configs = load_all_yaml_configs(root / "config")

# Backwards-compatible individual variables (optional)
logGroupCfg = configs.get("log_groups", {})
systemCfg = configs.get("systems", {})


app = cdk.App()
AwsMonitorCdkStack(app, "AwsMonitorCdkStack", configs=configs,
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
