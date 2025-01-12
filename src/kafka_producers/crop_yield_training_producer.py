from kafka import KafkaProducer
import pandas as pd
import json
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BROKER = 'localhost:9093'
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

try:
    data = pd.read_csv(csv_file)
    logger.info(f"Loaded {len(data)} rows from {csv_file}")
except FileNotFoundError as e:
    logger.error(f"File not found: {csv_file}")
    raise e

# Handle NaN values by replacing them with None for JSON serialization
data = data.where(pd.notnull(data), None)

# Stream rows to Kafka topic
for index, row in data.iterrows():
    message = row.to_dict()
    try:
        producer.send(TOPIC, message)
        logger.info(f"Produced row {index} to topic {TOPIC}")
        time.sleep(0.1)
    except Exception as e:
        logger.error(f"Failed to send message: {message}. Error: {e}")

# Flush and close the producer
producer.flush()
producer.close()
logger.info("Kafka producer closed.")
