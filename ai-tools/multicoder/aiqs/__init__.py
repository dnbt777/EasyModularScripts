from aiqs.ModelInterface import ModelInterface
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Now you can access the environment variables
aws_region = os.getenv("AWS_REGION")
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_username = os.getenv("AWS_USERNAME")
openai_api_key = os.getenv("OPENAI_API_KEY")
