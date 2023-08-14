from blocklineage import SnowflakeLineageBlock
import dotenv
import os

dotenv.load_dotenv(".env")

lb0 = SnowflakeLineageBlock(
    account=os.getenv("SF_ACCOUNT"),
    user=os.getenv("SF_USER"),
    password=os.getenv("SF_PASSWORD"),
    database=os.getenv("SF_DB"),
    db_schema=os.getenv("SF_SCHEMA"),
    role=os.getenv("SF_ROLE"),
    warehouse=os.getenv("SF_WAREHOUSE"),
)

lb0.save('sfax', overwrite=True)