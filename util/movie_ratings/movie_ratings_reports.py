import os
import sys
import logging
import logging.config
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from movie_sql_queries import COUNT_REVIEWS_PER_USER, MOST_REVIEWS_MOVIES

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

def generate_csv_reports_to_local(user_report_filename: str, movie_report_filename: str) -> list[str]:
    username = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    dbname = os.getenv('POSTGRES_DB')

    # Create a connection to PostgreSQL deployment instance
    connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}'
    logger.info(f"Attempting to connect to PostgreSQL at: {connection_string}")
    postgres_engine = create_engine(connection_string)

    # Execute queries and save results into local file system
    logger.info("Collecting reviews on a user basis")
    user_review_count = pd.read_sql_query(COUNT_REVIEWS_PER_USER, postgres_engine)
    local_user_report_path = os.path.join(root_dir, '_data', user_report_filename)
    user_review_count.to_csv(local_user_report_path)

    logger.info("Collecting reviews on a movie basis")
    movie_review_count = pd.read_sql_query(MOST_REVIEWS_MOVIES, postgres_engine)
    local_movie_report_path = os.path.join(root_dir, '_data', movie_report_filename)
    movie_review_count.to_csv(local_movie_report_path)

    return [local_user_report_path, local_movie_report_path]

def send_report_to_s3(file_names: list[str]) -> None:

    logger.info(f"Establishing connection to S3 Bucket")
    s3_client = S3Boto(os.getenv('AWS_S3_CONN_URL'), os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY'))

    for file in file_names:
        file_name, _ = os.path.splitext(os.path.basename(file))
        
        logger.info(f"Saving file: {file_name} to S3 Bucket")
        s3_client.upload_file(file, os.getenv('AWS_S3_BUCKET_NAME'), file_name)

