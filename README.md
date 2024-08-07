# Data Engineering Pipeline Sample using Apach Airflow
This is a sample configuration project that relies on Apache Airflow, AWS Localstack simulation for S3 file storage and PostgreSQL for data ingestion, processing, and reporting.
The project models a DAG (Directed Acyclic Graph) composed of tasks that sense file uploads on S3 storage, dump the content of these files onto SQL tables, run processing queries
on these tables and further return to S3 storage reports. This proof of work pipeline could be extended to a model that predicts daily provisioning of data that requires processing
and generaing reports on the data.
The pipeline has been containerized via Docker, using docker compose.

## Setup
Clone the repository via
```
git clone https://github.com/dlalaj/de_airflow.git
```
You will need to ensure you have Docker installed to be able to run the microservices. If you do not have it installed you can follow the official installation guide from the 
Docker [website](https://docs.docker.com/engine/install/) based on your operating system. You might need to allocate more memory for Docker if you are running into issues with 
starting the containers.

## About secrets and environment variables
To ensure all services run and the Docker images are built without running into any issues you need to provide a handful of environment variables that are used to configure airflow 
as well as the rest of the microservices. In particular you will need a `.env` and a `airflow_creds.env` file under the project root.

**NOTE THAT IN PRODUCTION ENVIRONMENTS THESE FILES WOULD NEVER BE SHARED IN PUBLIC OR SOME SECRET VAULT WOULD BE USED INSTEAD**

To ease your setup, you can use the following:

1. Airflow credentials used to build airflow images: `airflow_creds.env`

```
export AIRFLOW_USERNAME='airflow'
export AIRFLOW_FIRSTNAME='airflow'
export AIRFLOW_LASTNAME='airflow'
export AIRFLOW_ROLE='Admin'
export AIRFLOW_EMAIL='airflow@user.com'
export AIRFLOW_PASSWORD='airflow'
```
2. Environment variables used to set up microservices and connections from Airflow: `.env`

```
# S3 Boto AWS 
AWS_S3_CONN_URL='http://localstack:4566'
AWS_ACCESS_KEY_ID='test'
AWS_SECRET_ACCESS_KEY='test'
AWS_S3_BUCKET_NAME='movies'

# Logging configuration path
LOGGER_CONFIG_PATH='config/logging.conf'

# PostgreSQL configuration
POSTGRES_USER='psql_root'
POSTGRES_PASSWORD='psql_pw'
POSTGRES_DB='airflow_db'
POSTGRES_HOST='postgres_db'
POSTGRES_PORT=5432

# Airflow Connection IDs
PSQL_AIRFLOW_CONN_ID='psql_conn'
S3_AIRFLOW_CONN_ID='aws_s3_conn'
```

## Building the microservices
A Makefile has been provided to facilitate starting and interacting with the containers. To build the images enter the following from the command line. This will build the images for
all microservices and unless you make changes to the `Dockerfile` or the `docker-compose.yaml` file you should not need to run this command again.
```
make build-airflow
```

## Running the microservices
After the images have been built, they are ready to start up as containers running their corresponding services. To run the containers you can use this:
```
make start-airflow
```

## Connecting to the containers
You might sometimes find it necessary to connect to the containers as they are running for debugging purposes or to check table schemas and database state. You can connect to the
airflow or the postgres container after they have started using the following commands:
```
make connect-airflow         # Connects to the Airflow container which is running the webserver and the scheduler
make connect-psql            # Connects to the PostgreSQL container which is running the database server
```

