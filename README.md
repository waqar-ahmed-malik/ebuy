# Apache Airflow and DBT using Docker Compose
Stand-alone project that utilises custom streaming app to generate events to demonstrate how to schedule dbt models 
through Airflow

## Requirements 
* Install [Docker](https://www.docker.com/products/docker-desktop)
* Install [Docker Compose](https://docs.docker.com/compose/install/)

## Setup 
* Clone the repository
* Change directory within the repository
* Run:- docker compose build
* Run:- docker compose up 
 This includes the following services:
  * postgres-airflow: DB for Airflow to connect and store task execution information
  * postgres-dbt: DB for the DBT seed data and SQL models to be stored
  * airflow: Python-based image to execute Airflow scheduler and webserver
  * adminer: a lightweight DB client
  * streamlit: Python-based module to create interactive web apps

## Connections
* Adminer UI: http://localhost:8080
* Airflow UI: http://localhost:8000
* Streamlit UI: http://localhost:8501
* Airflow credentials to login
  -User = admin
  -Pass = admin
* adminer credentials to login
  -Database=dbtdb,
  -User=dbtuser,
  -Password=pssd,
  -Host=postgres-dbt,

Once everything is up and running, navigate to the Airflow UI (see connections above). You will be presented with the list of DAGs.

## Steps to generate Events using streamlit 
* navigate to localhost http://localhost:8501
* to generate events click on the button ingest_events
* According to the events_type:[Login, Register, Purchase]

## Steps to run the dags
* navigate to the Airflow UI 
* execute dag `full_referesh_dag` Once
* execute dag `ingest_bronze_dbt_data`
* executing the dag `ingest_bronze_dbt_data` will also trigger dependent dags with silver and gold layer models of dbt
If everything goes well, you should have the models execute successfully
Finally, within Adminer you can view the final models.