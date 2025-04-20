import requests
import json
from datetime import datetime
import time
from confluent_kafka import Producer

def get_data():
    response = requests.get("https://randomuser.me/api/")
    data = response.json()
    res = data['results'][0]
    return res

def format_data(res):
    data = {}
    location = res["location"]
    
    dob = datetime.fromisoformat(res['dob']['date'].replace('Z', '+00:00'))
    registered = datetime.fromisoformat(res['registered']['date'].replace('Z', '+00:00'))
    
    data["first_name"] = res["name"]["first"]
    data["last_name"] = res["name"]["last"]
    data["gender"] = res["gender"]
    data["address"] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                     f"{location['city']}, {location['state']}, {location['country']}"
    data['postcode'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = dob.strftime("%Y-%m-%d")  
    data['registered_date'] = registered.strftime("%Y-%m-%d")  
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def stream_data():
    # Configure Kafka producer
    conf = {
        'bootstrap.servers': 'localhost:9092',
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
    
    # Wait for any outstanding messages to be delivered
    producer.flush()

if __name__ == "__main__":
    stream_data() 