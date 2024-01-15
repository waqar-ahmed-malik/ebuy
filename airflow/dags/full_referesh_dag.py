from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1)
}

dag = DAG('ingest_full_load_data', default_args=default_args, catchup=False, schedule_interval=None)

ingest_full_referesh_data = BashOperator(
    task_id='ingest_full_referesh_data',
    bash_command='dbt run --select events -f --profiles-dir /dbt --project-dir /dbt',
    dag=dag
)

ingest_full_referesh_data