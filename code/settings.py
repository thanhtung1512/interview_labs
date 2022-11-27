import logging
# Parameters for main function
CIDR_IP = [{'CidrIp': '0.0.0.0/0'}]
SSH_PORT_NUMBER = 22 # Default port 22
TAG_NAME = 'Allow_ssh_all'
TAG_VALUE = 'True' 
REGIONS = ["us-east-1", "ap-northeast-1"] # Add more regions here in case of you need to scan
# REGIONS = ["us-east-1"] # Add more regions here in case of you need to scan
LOGGING_LEVEL = logging.INFO # Set level log for logging