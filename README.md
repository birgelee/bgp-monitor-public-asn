# bgp-monitor-public-asn
Monitor BGP announcements and get alerted if an asn shows up in the path


Dependencies:
websocket-client:
Install with:
python3 -m pip install websocket-client --break-system-packages

boto3:
Install and configure the AWS CLI with the region of the AWS SNS topic needed for the default profile (~/.aws/config). Make sure the default profile has access credentials for the SNS Topic (~/.aws/credentials).
Install boto3 with:
python3 -m pip install boto3 --break-system-packages
