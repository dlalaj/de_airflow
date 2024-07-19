import os
import sys
from datetime import timedelta
from dotenv import load_dotenv
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.operators.python import PythonOperator

# Add project root dir to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.movie_ratings.movie_ratings_processing import load_data_to_database

# Load environment variables
load_dotenv()

# Set up default arguments for dag
default_args = {
    'owner': 'dionysus',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False
}

print(os.getenv('AWS_S3_BUCKET_NAME'))

with DAG(dag_id='movie_ratings_csv_process_and_report', 
        default_args=default_args, 
        schedule=None, 
        is_paused_upon_creation=True) as dag:
    
    csv_names = ['movies.csv', 'users.csv', 'movieratings.csv']

    # Airflow S3 Sensors to detect upload for new movie ratings
    detect_s3_movie_csv_upload = S3KeySensor(task_id='detect_s3_upload_movie',
                                        bucket_name=os.getenv('AWS_S3_BUCKET_NAME'),
                                        bucket_key=csv_names[0], 
                                        aws_conn_id=os.getenv('S3_AIRFLOW_CONN_ID'), 
                                        timeout=60*60, 
                                        poke_interval=60)
    
    detect_s3_user_csv_upload = S3KeySensor(task_id='detect_s3_upload_user',
                                    bucket_name=os.getenv('AWS_S3_BUCKET_NAME'),
                                    bucket_key=csv_names[1], 
                                    aws_conn_id=os.getenv('S3_AIRFLOW_CONN_ID'), 
                                    timeout=60*60, 
                                    poke_interval=60)
    
    detect_s3_rating_csv_upload = S3KeySensor(task_id='detect_s3_upload_ratings',
                                bucket_name=os.getenv('AWS_S3_BUCKET_NAME'),
                                bucket_key=csv_names[2], 
                                aws_conn_id=os.getenv('S3_AIRFLOW_CONN_ID'), 
                                timeout=60*60, 
                                poke_interval=60)

    # Record new movies and reviews onto PostgreSQL
    read_csvs_to_db = PythonOperator(task_id='read_csv_to_db',
                                    python_callable=load_data_to_database,
                                    op_args=[csv_names, os.getenv('AWS_S3_BUCKET_NAME')])

    # Define task dependencies
    [detect_s3_movie_csv_upload, detect_s3_user_csv_upload, detect_s3_rating_csv_upload] >> read_csvs_to_db
