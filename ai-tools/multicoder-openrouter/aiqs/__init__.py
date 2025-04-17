
from aiqs.ModelInterface import ModelInterface
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Now you can access the environment variables
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
