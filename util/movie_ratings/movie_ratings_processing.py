import os
import sys
import logging
import logging.config
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Add util dir to path to import S3Boto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from s3bucket import S3Boto

# Read environment variables
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(root_dir, '.env'))

# Configure logging
logger_conf_dir = os.path.join(root_dir, os.getenv('LOGGER_CONFIG_PATH'))
logging.config.fileConfig(logger_conf_dir)
logger = logging.getLogger()

def read_csv_from_s3(file_name: str, bucket_name: str) -> pd.DataFrame:
    # Read CSV content from S3 bucket, assuming small CSV file that can be loaded to memory to avoid local download
    s3_client = S3Boto(os.getenv('AWS_S3_CONN_URL'), os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY'))
    file_content = s3_client.read_file(bucket_name, file_name)

    # Put content into pandas dataframe
    df = pd.read_csv(StringIO(file_content))
    df = df.dropna()

    return df

def dump_csv_to_db(df: pd.DataFrame, table_name: str) -> None:
    # Read PostgreSQL database details from environment variables
    username = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    dbname = os.getenv('POSTGRES_DB')

    # Create a connection to PostgreSQL deployment instance
    connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}'
    logger.info(f"Attempting to connect to PostgreSQL at: {connection_string}")
    postgres_engine = create_engine(connection_string)

    logger.info(f"Writing new data to: {table_name}")
    # Write dataframe content to database
    df.to_sql(table_name, postgres_engine, if_exists='append', index=False)


def load_data_to_database(files: list[str], bucket: str) -> None:

    for file in files:
        logger.info(f"Attempting to load to database file: {file}")

        data = read_csv_from_s3(file_name=file, bucket_name=bucket)
        # Yield table name from csv filename
        table_name, _ = os.path.splitext(os.path.basename(file))
        dump_csv_to_db(data, table_name)

        logger.info(f"File: {file} loaded to database successfully")
