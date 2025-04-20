from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from kafka_producer import get_data, format_data
from confluent_kafka import Producer
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_to_kafka():
    # Configure Kafka producer
    conf = {
        'bootstrap.servers': 'broker:29092',  # Use internal Docker network address
        'client.id': 'python-producer'
    }
    
    producer = Producer(conf)
    
    try:
        user = get_data()
        formatted_data = format_data(user)
        
        json_data = json.dumps(formatted_data)
        
        producer.produce('users_created', 
                       value=json_data.encode('utf-8'),
                       callback=delivery_report)
        producer.poll(0)
        
        print("\nProduced User Data:")
        print("==================")
        print(json.dumps(formatted_data, indent=4, ensure_ascii=False))
        print("==================\n")
        
    except Exception as e:
        print(f"Error: {e}")
        raise e
    finally:
        # Wait for any outstanding messages to be delivered
        producer.flush()

with DAG(
    'kafka_stream_dag',
    default_args=default_args,
    description='A DAG to stream data to Kafka',
    schedule_interval=timedelta(minutes=5),
    catchup=False
) as dag:

    produce_task = PythonOperator(
        task_id='produce_to_kafka',
        python_callable=produce_to_kafka,
    ) 