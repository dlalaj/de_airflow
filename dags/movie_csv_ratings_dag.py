import os
import sys
from datetime import timedelta
from dotenv import load_dotenv
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python import PythonOperator

# Add project root dir to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
from util.movie_ratings.movie_ratings_processing import load_data_to_database
from util.movie_ratings.movie_ratings_reports import generate_csv_reports_to_local, send_report_to_s3

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
    
    # TODO: Below it would be best that the parameters to 'send_report_to_s3' are not hardcoded but are 
    # instead piped from 'generate_csv_reports_to_local' via XComs, perhaps can consider in the future.

    generate_report = PythonOperator(task_id='generate_csv_reports',
                                     python_callable=generate_csv_reports_to_local,
                                     op_args=[['user_review_count.csv', 'movie_review_count.csv']])
    
    save_reports_to_S3 = PythonOperator(task_id='save_reports_to_S3',
                                        python_callable=send_report_to_s3,
                                        op_args=[[os.path.join(root_dir, '_data/user_review_count.csv'),
                                                  os.path.join(root_dir, '_data/movie_review_count.csv')]])

    # Define task dependencies
    [detect_s3_movie_csv_upload, detect_s3_user_csv_upload, detect_s3_rating_csv_upload] >> read_csvs_to_db
    read_csvs_to_db >> generate_report >> save_reports_to_S3
