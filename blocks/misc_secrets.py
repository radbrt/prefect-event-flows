from prefect.blocks.system import Secret
import os
from dotenv import load_dotenv

load_dotenv('.env')

apikey = os.getenv("OPENAI_API_KEY")

openai = Secret(value=apikey)
openai.save("openai-api-key", overwrite=True)