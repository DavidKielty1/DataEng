from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import requests
import json
import logging

# Set Airflow task logging to ERROR level to reduce verbosity
logging.getLogger('airflow.task').setLevel(logging.ERROR)

def get_data():
    response = requests.get("https://randomuser.me/api/")
    data = response.json()
    res = data['results'][0]
    return res

def format_data(res):
    data = {}
    location = res["location"]
    data["first_name"] = res["name"]["first"]
    data["last_name"] = res["name"]["last"]
    data["gender"] = res["gender"]
    data["address"] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                     f"{location['city']}, {location['state']}, {location['country']}"
    data['postcode'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data

def stream_data():
    # Disable other loggers
    for logger_name in ['airflow.task', 'airflow.dag', 'airflow']:
        logging.getLogger(logger_name).setLevel(logging.ERROR)
    
    user = get_data()
    formatted_data = format_data(user)
    # Only print our formatted data
    print("\nFormatted User Data:")
    print("==================")
    print(json.dumps(formatted_data, indent=4))
    print("==================\n")
    return formatted_data

default_args = {
    'owner': 'David Kielty',
    'start_date': datetime.now() - timedelta(days=1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

with DAG(
    dag_id='kafka_stream',
    default_args=default_args,
    description='A simple Kafka stream DAG',
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    streaming_task = PythonOperator(
        task_id='streaming_data_from_api',
        python_callable=stream_data,
    )
