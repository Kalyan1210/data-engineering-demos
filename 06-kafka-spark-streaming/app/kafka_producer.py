import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC_USER_EVENTS = 'user_events'
TOPIC_SENSOR_DATA = 'sensor_data'
TOPIC_TRANSACTIONS = 'transactions'

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_user_event():
    """Generate sample user event data"""
    events = ['page_view', 'click', 'purchase', 'login', 'logout']
    return {
        'user_id': random.randint(1, 1000),
        'event_type': random.choice(events),
        'timestamp': datetime.now().isoformat(),
        'page_url': f'/page/{random.randint(1, 50)}',
        'session_id': f'session_{random.randint(1000, 9999)}'
    }

def generate_sensor_data():
    """Generate sample sensor data"""
    return {
        'sensor_id': f'sensor_{random.randint(1, 10)}',
        'temperature': round(random.uniform(20, 30), 2),
        'humidity': round(random.uniform(40, 80), 2),
        'pressure': round(random.uniform(1000, 1100), 2),
        'timestamp': datetime.now().isoformat()
    }

def generate_transaction():
    """Generate sample transaction data"""
    return {
        'transaction_id': f'txn_{random.randint(10000, 99999)}',
        'user_id': random.randint(1, 1000),
        'amount': round(random.uniform(10, 1000), 2),
        'currency': random.choice(['USD', 'EUR', 'GBP']),
        'merchant': f'merchant_{random.randint(1, 20)}',
        'timestamp': datetime.now().isoformat()
    }

def produce_data():
    """Produce data to Kafka topics"""
    try:
        while True:
            # Produce user events
            user_event = generate_user_event()
            producer.send(TOPIC_USER_EVENTS, user_event)
            print(f"Sent user event: {user_event['event_type']}")

            # Produce sensor data
            sensor_data = generate_sensor_data()
            producer.send(TOPIC_SENSOR_DATA, sensor_data)
            print(f"Sent sensor data: {sensor_data['sensor_id']}")

            # Produce transaction data
            transaction = generate_transaction()
            producer.send(TOPIC_TRANSACTIONS, transaction)
            print(f"Sent transaction: {transaction['transaction_id']}")

            time.sleep(2)  # Send data every 2 seconds

    except KeyboardInterrupt:
        print("Stopping data production...")
        producer.close()

if __name__ == "__main__":
    print("Starting Kafka data producer...")
    produce_data() 