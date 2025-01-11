from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when, monotonically_increasing_id, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CropYieldPreprocessing") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

# Define schema for Kafka messages
kafka_schema = StructType([
    StructField("week_start_date", StringType(), True),
    StructField("week_end_date", StringType(), True),
    StructField("region", StringType(), True),
    StructField("state", StringType(), True),
    StructField("district", StringType(), True),
    StructField("field_id", StringType(), True),
    StructField("crop_id", StringType(), True),
    StructField("crop_name", StringType(), True),
    StructField("crop_type", StringType(), True),
    StructField("crop_season", StringType(), True),
    StructField("soil_nitrogen_ppm", FloatType(), True),
    StructField("soil_phosphorus_ppm", FloatType(), True),
    StructField("soil_potassium_ppm", FloatType(), True),
    StructField("npk_ratio", StringType(), True),
    StructField("soil_moisture_percent", FloatType(), True),
    StructField("crop_rotation_previous_crop", StringType(), True),
    StructField("rainfall_mm", FloatType(), True),
    StructField("temperature_celsius", FloatType(), True),
    StructField("humidity_percent", FloatType(), True),
    StructField("solar_radiation_mj_per_m2", FloatType(), True),
    StructField("wind_speed_kmph", FloatType(), True),
    StructField("fertilizer_used", StringType(), True),
    StructField("pesticide_used", StringType(), True),
    StructField("pesticide_quantity_liters_per_hectare", FloatType(), True),
    StructField("yield_kg_per_hectare", FloatType(), True),
    StructField("market_price_per_kg", FloatType(), True),
    StructField("crop_inflation_percent", FloatType(), True),
    StructField("profitability_index", FloatType(), True),
    StructField("market_demand_tons", FloatType(), True),
    StructField("export_potential_tons", FloatType(), True),
    StructField("climate_risk_index", FloatType(), True)
])

# Read from Kafka
kafka_source = {
    "kafka.bootstrap.servers": "kafka-broker1:9092",
    "subscribe": "crop-yield-topic"
}
raw_stream = spark.readStream.format("kafka") \
    .options(**kafka_source) \
    .load()

# Parse Kafka messages
parsed_stream = raw_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), kafka_schema).alias("data")) \
    .select("data.*")

# Real-time preprocessing: Add derived columns
processed_stream = parsed_stream.withColumn("climate_risk_index", 
    col("rainfall_mm") * 0.5 + col("temperature_celsius") * 0.3)

# Write preprocessed data to HDFS
hdfs_sink = "hdfs://namenode:9000/druid/processed_data"
processed_stream.writeStream \
    .format("parquet") \
    .option("path", hdfs_sink) \
    .option("checkpointLocation", hdfs_sink + "/checkpoints") \
    .start()

# Batch processing: Create dimensions and fact table
# Read preprocessed data from HDFS
df = spark.read.parquet(hdfs_sink)

# Create dimensions and fact table
time_dim = df.select(
    "week_start_date", "week_end_date"
).distinct().withColumn("week_id", monotonically_increasing_id())

field_dim = df.select(
    "field_id", "soil_nitrogen_ppm", "soil_phosphorus_ppm", "soil_potassium_ppm",
    "npk_ratio", "soil_moisture_percent", "crop_rotation_previous_crop"
).distinct()

crop_dim = df.select(
    "crop_id", "crop_name", "crop_type", "crop_season", 
    "fertilizer_used", "pesticide_used", "pesticide_quantity_liters_per_hectare"
).distinct()

region_dim = df.select(
    "region", "state", "district"
).distinct().withColumn("region_id", monotonically_increasing_id())

climate_dim = df.select(
    "week_start_date", "rainfall_mm", "temperature_celsius", 
    "humidity_percent", "solar_radiation_mj_per_m2", 
    "wind_speed_kmph", "climate_risk_index"
).distinct()

market_dim = df.select(
    "week_start_date", "market_price_per_kg", "crop_inflation_percent"
).distinct()

fact_table = df.join(time_dim, ["week_start_date", "week_end_date"]) \
    .join(region_dim, ["region", "state", "district"]) \
    .select(
        col("week_id"), col("field_id"), col("crop_id"), col("region_id"),
        col("yield_kg_per_hectare"), col("profitability_index"),
        col("market_demand_tons"), col("export_potential_tons")
    )

# Write dimensions and fact table to HDFS
time_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/time_dim")
field_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/field_dim")
crop_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/crop_dim")
region_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/region_dim")
climate_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/climate_dim")
market_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/market_dim")
fact_table.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/crop_yield_fact")

# Keep the streaming job running
spark.streams.awaitAnyTermination()
