from prefect import flow, task
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import pandas as pd
import re
import datetime
from blocklineage import SnowflakeLineageBlock
import blocklineage
from prefect.artifacts import create_markdown_artifact
import marvin
from marvin import ai_fn
from prefect.blocks.system import Secret





@task
def get_latest_interest_data(block: SnowflakeLineageBlock) -> pd.DataFrame:
    
    df = block.read_sql('select * from unemployment')
    return df

@ai_fn
def analyze_unemployment_data(df: pd.DataFrame) -> str:
    """Analyze unemployment data and return a 
    markdown-formatted string."""


@task
def make_unemployment_report(df):
    
    secret_block = Secret.load("openai-api-key")
    marvin.settings.openai.api_key = secret_block.get()

    markdown_report = analyze_unemployment_data(df)

    create_markdown_artifact(
        key="ai-unemployment-report",
        markdown=markdown_report,
        description="Monthly unemployment report",
    )


@flow
def update_unemployment_report():
    block = SnowflakeLineageBlock.load('sfax')
    df = get_latest_interest_data(block)
    make_unemployment_report(df)
