import os
import json
from datetime import datetime

# Directory path containing CSV files
folder_path = "/path/to/csv/files"
output_path = "./generated_configs"
os.makedirs(output_path, exist_ok=True)

# Kafka and Druid Settings
kafka_broker = "kafka-broker1:9092"
def get_druid_parallelism(file_size_mb):
    if file_size_mb < 100:
        return 1  # Small files
    elif file_size_mb < 1000:
        return 4  # Medium files
    else:
        return 8  # Large files

def generate_kafka_connector(file_path, topic_name):
    connector_config = {
        "name": f"{topic_name}-connector",
        "config": {
            "connector.class": "FileStreamSource",
            "tasks.max": "1",
            "file": file_path,
            "topic": topic_name,
            "key.converter": "org.apache.kafka.connect.storage.StringConverter",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "value.converter.schemas.enable": "false",
            "key.converter.schemas.enable": "false",
            "file.poll.interval.ms": "1000"
        }
    }
    return connector_config

def generate_druid_config(topic_name, dimensions, parallelism):
    druid_config = {
        "type": "index_parallel",
        "spec": {
            "dataSchema": {
                "dataSource": topic_name,
                "timestampSpec": {
                    "column": "date",
                    "format": "auto"
                },
                "dimensionsSpec": {
                    "dimensions": dimensions
                }
            },
            "ioConfig": {
                "type": "kafka",
                "topic": topic_name,
                "consumerProperties": {
                    "bootstrap.servers": kafka_broker
                },
                "inputFormat": {
                    "type": "csv",
                    "findColumnsFromHeader": True
                }
            },
            "tuningConfig": {
                "type": "index_parallel",
                "maxNumConcurrentSubTasks": parallelism,
                "forceGuaranteedRollup": False
            }
        }
    }
    return druid_config

def infer_columns(file_path):
    with open(file_path, 'r') as f:
        header_line = f.readline().strip()
        columns = header_line.split(',')
    return columns

def main():
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            topic_name = os.path.splitext(file_name)[0].replace(" ", "_").lower()

            # Get file size in MB
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

            # Infer dimensions from CSV header
            dimensions = infer_columns(file_path)

            # Determine parallelism based on file size
            parallelism = get_druid_parallelism(file_size_mb)

            # Generate Kafka Connect configuration
            kafka_config = generate_kafka_connector(file_path, topic_name)
            kafka_config_path = os.path.join(output_path, f"{topic_name}_kafka_connector.json")
            with open(kafka_config_path, 'w') as f:
                json.dump(kafka_config, f, indent=4)

            # Generate Druid configuration
            druid_config = generate_druid_config(topic_name, dimensions, parallelism)
            druid_config_path = os.path.join(output_path, f"{topic_name}_druid_config.json")
            with open(druid_config_path, 'w') as f:
                json.dump(druid_config, f, indent=4)

            print(f"Generated configs for {file_name}:\n  - {kafka_config_path}\n  - {druid_config_path}")

if __name__ == "__main__":
    main()
