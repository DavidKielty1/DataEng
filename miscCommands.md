source .venv/Scripts/activate

MSYS_NO_PATHCONV=1 docker-compose exec broker python3 /opt/airflow/dags/kafka_stream.py