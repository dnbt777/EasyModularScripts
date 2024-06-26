# initializes loading of dotenv and stuff
from aiqs import *

# initialize the model interface
# automatically makes bedrock client, openai client, and cost tracker
modelinterface = ModelInterface()

prompt = "Introduce yourself, with enthusiasm! Keep it short though and use emojis!"

if all([aws_region, access_key, secret_key, aws_username]):
    for model in "haiku sonnet opus".split():
        response = modelinterface.send_to_ai(prompt, model=model)
        modelinterface.cost_tracker.show_cost_data()

if openai_api_key:
    for model in "gpt-4o gpt-3.5-turbo".split():
        response = modelinterface.send_to_ai(prompt, model=model, max_tokens=500, temperature=1.3)
        print(response[0], '\n')