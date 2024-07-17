from airflow import settings
from airflow.models import Connection

conn = Connection(
        conn_id='<CHOOSE>',
        conn_type='<CHOOSE>',
        host='<CHOOSE>',
        login='<CHOOSE>',
        password='<CHOOSE>',
        port='<CHOOSE>', # Needs to be integer
        schema='<CHOOSE>'
)

# Add new connection to airflow connections
session = settings.Session()
session.add(conn)
session.commit()
