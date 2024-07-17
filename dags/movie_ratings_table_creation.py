import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# Add
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.create_sql_tables import *

# Set up default arguments for dag
default_args = {
    'owner': 'dionysus',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False
}

# Use context manager to define DAG for table creation, manually triggered from Airflow UI
with DAG(dag_id='create_movie_user_ratings_sql_tables', 
        default_args=default_args, 
        schedule=None, 
        is_paused_upon_creation=True) as dag:

    # Define DAG tasks
    create_movies_table = SQLExecuteQueryOperator(task_id='create_movie_table', conn_id='psql_conn', sql=CREATE_movies_TABLE)
    create_user_table = SQLExecuteQueryOperator(task_id='create_user_table', conn_id='psql_conn', sql=CREATE_users_TABLE)
    create_ratings_table = SQLExecuteQueryOperator(task_id='create_rating_table', conn_id='psql_conn', sql=CREATE_ratings_TABLE)

    # Define task dependencies
    [create_movies_table, create_user_table] >> create_ratings_table
