from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1)
}

dag = DAG('ingest_silver_dbt_data', default_args=default_args, catchup=False, schedule_interval=None)

execute_silver_models = BashOperator(
    task_id='execute_silver_models',
    bash_command='dbt run --select user_metrics --profiles-dir /dbt --project-dir /dbt',
    dag=dag
)

trigger_gold_models = TriggerDagRunOperator(
  task_id="trigger_gold_models",
  trigger_dag_id="ingest_gold_dbt_data",
  dag=dag
)

execute_silver_models >> trigger_gold_models
