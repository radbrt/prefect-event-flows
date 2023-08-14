from prefect import flow, task
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import pandas as pd
import re
import datetime
from blocklineage import SnowflakeLineageBlock
import blocklineage


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    # Replace spaces and special characters with underscores
    df.columns = [re.sub(r'\W+', '_', col.strip().lower()) for col in df.columns]
    return df


@task
def download_unemployment_data() -> pd.DataFrame:
    df = pd.read_csv('https://data.ssb.no/api/v0/dataset/1052.csv?lang=en', sep=',')
    df = clean_column_names(df)
    df = df.rename(columns={df.columns[-1]: 'unemployment_rate'})
    extracted_at = datetime.datetime.now()
    df["extracted_at"] = extracted_at
    return df


@task
def filter_adjustment(df: pd.DataFrame, adjustment_type) -> pd.DataFrame:
    df = df[df['type_of_adjustment'] == adjustment_type]
    return df


# @task
# def save_to_db(df: pd.DataFrame):
#     sfblock = SnowflakeLineageBlock.load('sfax')
#     df.lb.to_sql('unemployment', sfblock, if_exists='append', index=False)


@flow
def load_unemployment_data(adjustment_type='S Seasonally adjusted'):
    df = download_unemployment_data()
    df = filter_adjustment(df, adjustment_type)
    sfblock = SnowflakeLineageBlock.load('sfax')
    df.lb.to_sql('unemployment', con=sfblock, if_exists='replace', index=False)


if __name__ == '__main__':
    load_unemployment_data()
