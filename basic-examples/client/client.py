# Use the Converse API to send a text message to Llama 2 Chat 70B.
import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from dotenv import load_dotenv

load_dotenv()

import boto3

from custom_logger import logger

# Create a Bedrock Runtime client in the AWS Region you want to use.
logger.info("Initializing client...")
client = boto3.client(
    service_name=os.getenv("AWS_SERVICE_NAME"),
    region_name=os.getenv("AWS_REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
logger.info("Initialization of client Done")
