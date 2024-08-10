import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

MODEL_TITAN_G_1_PREMIER = "amazon.titan-text-premier-v1:0"
MODEL_COHERE_COMMAND_R_PLUS = "cohere.command-r-plus-v1:0"
MODEL_LLAMA_3_1_8B = "meta.llama3-1-8b-instruct-v1:0"
MODEL_LLAMA_3_1_70B = "meta.llama3-1-70b-instruct-v1:0"
MODEL_LLAMA_3_1_405B = "meta.llama3-1-405b-instruct-v1:0"
MODEL_MISTRAL_LARGE = "mistral.mistral-large-2402-v1:0"

SERVICE_NAME = "bedrock-runtime"
AVAILABLE_REGIONS = ["us-east-1", "us-west-2"]
