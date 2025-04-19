from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'David Kielty',
    'start_date': datetime(2025, 4, 19, 15, 00),
}

def stream_data():
    import json
    import requests

    response = requests.get("https://randomeruser.me/api/")
    data = response.json()
    print(data)

with DAG(
    dag_id='kafka_stream',
    default_args=default_args,
    description='A simple Kafka stream DAG',
    schedule_interval='@daily',
) as dag:
    
    streaming_task = PythonOperator(
        task_id='streaming_data_from_api',
        python_callable=stream_data,
    )

stream_data();
