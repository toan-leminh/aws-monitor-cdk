
# Welcome to your CDK Python project!

Require
  Python version >= 3.11

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk destroy`     remote this stack resources
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

## Run Project
source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

## Project struture
aws-monitor-cdk/
│
├── app.py
├── stacks/
│   ├── monitoring_stack.py
│
├── constructs/
│   ├── log_groups.py
│   ├── alarms.py
│   ├── eventbridge_startstop.py
│   ├── cw_agent_ssm.py
│
├── config/
│   └── systems.yaml       # Chỉ khai báo tên hệ thống → không khai báo EC2
│
└── requirements.txt 
