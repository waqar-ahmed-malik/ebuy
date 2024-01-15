from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1)
}

dag = DAG('ingest_gold_dbt_data', default_args=default_args, catchup=False, schedule_interval=None)

execute_bronze_models = BashOperator(
    task_id='execute_bronze_models',
    bash_command='dbt run --select user_types --profiles-dir /dbt --project-dir /dbt',
    dag=dag
)

execute_bronze_models