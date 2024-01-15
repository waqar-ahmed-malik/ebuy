from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1)
}

dag = DAG('ingest_bronze_dbt_data', default_args=default_args, catchup=False, schedule_interval=timedelta(days=1))

execute_bronze_models = BashOperator(
    task_id='execute_bronze_models',
    bash_command='dbt run --select events --profiles-dir /dbt --project-dir /dbt',
    dag=dag
)

trigger_silver_models = TriggerDagRunOperator(
  task_id="trigger_silver_models",
  trigger_dag_id="ingest_silver_dbt_data",
  dag=dag
)

execute_bronze_models >> trigger_silver_models