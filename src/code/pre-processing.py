from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when, monotonically_increasing_id

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CropYieldPreprocessing") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

# Load enhanced dataset
input_file = "/path/to/enhanced_indian_crop_yield_weekly_20_years.csv"
df = spark.read.csv(input_file, header=True, inferSchema=True)

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

# Create the fact table
fact_table = df.join(time_dim, ["week_start_date", "week_end_date"]) \
    .join(region_dim, ["region", "state", "district"]) \
    .select(
        col("week_id"), col("field_id"), col("crop_id"), col("region_id"),
        col("yield_kg_per_hectare"), col("profitability_index"),
        col("market_demand_tons"), col("export_potential_tons")
    )

# Write dimensions and fact table to HDFS in Parquet format
time_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/time_dim")
field_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/field_dim")
crop_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/crop_dim")
region_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/region_dim")
climate_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/climate_dim")
market_dim.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/market_dim")
fact_table.write.mode("overwrite").parquet("hdfs://namenode:9000/druid/crop_yield_fact")

# Stop Spark session
spark.stop()
