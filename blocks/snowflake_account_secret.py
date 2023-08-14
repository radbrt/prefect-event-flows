from prefect.blocks.system import Secret
import os
from dotenv import load_dotenv

load_dotenv('.env')

sfaccount = Secret(value=os.getenv("SNOWFLAKE_ACCOUNT"))

sfaccount.save("snowflake-account", overwrite=True)