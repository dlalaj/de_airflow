build-airflow:
	docker compose build

start-airflow:
	docker compose up

connect-airflow:
	docker exec -it apache_airflow bash

connect-psql:
	docker exec -it postgres_db bash
