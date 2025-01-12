from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_date
from pyspark.sql.types import StructType, StringType, DoubleType

# Kafka and HDFS configuration
KAFKA_TOPIC = "crop-data-topic"
KAFKA_BROKERS = "kafka:9092"
HDFS_PATH = "/hadoop/dfs/data/"

# Define schema for the input data
schema = StructType() \
    .add("week_start_date", StringType()) \
    .add("week_end_date", StringType()) \
    .add("region", StringType()) \
    .add("state", StringType()) \
    .add("district", StringType()) \
    .add("crop_name", StringType()) \
    .add("crop_type", StringType()) \
    .add("crop_season", StringType()) \
    .add("yield_kg_per_hectare", DoubleType()) \
    .add("rainfall_mm", DoubleType()) \
    .add("temperature_celsius", DoubleType()) \
    .add("humidity_percent", DoubleType()) \
    .add("market_price_per_kg", DoubleType()) \
    .add("climate_risk_index", DoubleType())

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaToHDFS") \
    .getOrCreate()

# Read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

# Parse Kafka value as JSON
df_parsed = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Transform data
df_transformed = df_parsed.select(
    col("region"),
    col("state"),
    col("district"),
    col("crop_name"),
    col("crop_type"),
    col("crop_season"),
    col("yield_kg_per_hectare"),
    col("rainfall_mm"),
    col("temperature_celsius"),
    col("humidity_percent"),
    col("market_price_per_kg"),
    col("climate_risk_index"),
    to_date(col("week_start_date"), "yyyy-MM-dd").alias("week_start_date")
)

# Write to HDFS
query = df_transformed.writeStream \
    .format("parquet") \
    .option("path", f"{HDFS_PATH}/streamed_transformed_data") \
    .option("checkpointLocation", f"{HDFS_PATH}/checkpoints/") \
    .outputMode("append") \
    .start()

query.awaitTermination()
