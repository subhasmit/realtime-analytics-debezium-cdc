from kafka import KafkaProducer
import pandas as pd
import json
import time
import os

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'crop-data-topic'

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Read CSV
# Get the absolute file path and resolve it
base_path = os.path.abspath(os.path.dirname(__file__))
csv_file = os.path.realpath(os.path.join(base_path, '../../datasets/enhanced_indian_crop_yield_weekly_20_years.csv'))
data = pd.read_csv(csv_file)

# Stream rows to Kafka topic
for index, row in data.iterrows():
    producer.send(TOPIC, row.to_dict())
    print(f"Produced row {index} to topic {TOPIC}")
    time.sleep(0.1)

producer.flush()
producer.close()
