FROM python:3.12.2

# Update image and install supervisord for process bootstrapping
RUN apt-get update -y && apt-get install -y supervisor

# Set up airflow home, where the project will be copied as well
ENV AIRFLOW_HOME=/airflow
WORKDIR ${AIRFLOW_HOME}/

# Copy project and airflow credentials
COPY . ./
COPY airflow_creds.env ${AIRFLOW_HOME}/airflow_creds.env

# Install python depedencies
RUN pip install -r requirements.txt

# Initialize database and toggle example dags off
RUN airflow db migrate
COPY ./config/airflow.cfg airflow.cfg

# Create admin user with provided credentials - run only once when image is built
# Destroy airflow credential file after build is complete
RUN . ${AIRFLOW_HOME}/airflow_creds.env \
  && airflow users create \
  --username ${AIRFLOW_USERNAME} \
  --firstname ${AIRFLOW_FIRSTNAME} \
  --lastname ${AIRFLOW_LASTNAME} \
  --role ${AIRFLOW_ROLE} \
  --email ${AIRFLOW_EMAIL} \
  --password ${AIRFLOW_PASSWORD} \
  && rm ${AIRFLOW_HOME}/airflow_creds.env

# Copy supervisord configuration file to set up webserver and scheduler for airflow
COPY  ./config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR ${AIRFLOW_HOME}/

# Expose airflow webserver UI port
EXPOSE 8080
