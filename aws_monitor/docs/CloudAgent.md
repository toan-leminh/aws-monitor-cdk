
For restart CloudWatchAgent and re-load config.json (Powershell)
& "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" `
  -a fetch-config `
  -m ec2 `
  -c file:"C:\Program Files\Amazon\AmazonCloudWatchAgent\config.json" `
  -s

For Linux
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file://opt/aws/amazon-cloudwatch-agent/bin/config.json -s

Note for fix 32 bit and 64 bit adapt (Command Prompt)
#mklink /D "C:\Program Files (x86)\Amazon\AmazonCloudWatchAgent" "C:\Program Files\Amazon\AmazonCloudWatchAgent"

Check log (Powershell)
#Get-Content "C:\ProgramData\Amazon\AmazonCloudWatchAgent\Logs\amazon-cloudwatch-agent.log" -Tail 100

Restart CloudWatchAgent
#Restart-Service AmazonCloudWatchAgent
#Stop-Service AmazonCloudWatchAgent
#Start-Service AmazonCloudWatchAgent


Setting CloudWatchAgent (config.json)
-Get Memory and Disk
"metrics": {
    "metrics_collected": {
        "LocalDisk": {
            "measurement": [
                {"name": "% Free Space", "rename": "disk_free_percent"}
            ],
            "metrics_collection_interval": 60,
            "resources": [
                "*"
            ]
        },
        "Memory": {
            "measurement": [
                {"name": "% Committed Bytes In Use", "rename": "mem_used_percent" }
            ],
            "metrics_collection_interval": 60
        }
    }
}

Options: 
disk_used_percent: % Disk Used
disk_available: Disk Available
mem_used_percent: % Memory Used
mem_available: Memory Available
 