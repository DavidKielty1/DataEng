A code along exposure to airflow, docker, kafka, spark data pipeline.

git add . && git commit -m 'First Commit' && git push origin main.


Architecture:
Apache Airflow DAG => Fetches data from randomuser.me
Streamed into kafka
Zookeeper manages kafka brokers
    visualized in control centre, schema registry
Data from kafka will be streamed into apache spark.
    master -> workers 
Data from spark will be streamed to cassandra

Docker compose will spin-up instances above.


