from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_USER_EVENTS = "user_events"
TOPIC_SENSOR_DATA = "sensor_data"
TOPIC_TRANSACTIONS = "transactions"

# Define schemas for different data types
user_events_schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("event_type", StringType()),
    StructField("timestamp", StringType()),
    StructField("page_url", StringType()),
    StructField("session_id", StringType())
])

sensor_data_schema = StructType([
    StructField("sensor_id", StringType()),
    StructField("temperature", DoubleType()),
    StructField("humidity", DoubleType()),
    StructField("pressure", DoubleType()),
    StructField("timestamp", StringType())
])

transactions_schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("user_id", IntegerType()),
    StructField("amount", DoubleType()),
    StructField("currency", StringType()),
    StructField("merchant", StringType()),
    StructField("timestamp", StringType())
])

def process_user_events():
    """Process user events stream"""
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", TOPIC_USER_EVENTS) \
        .load()
    
    # Parse JSON and apply schema
    parsed_df = df.select(
        from_json(col("value").cast("string"), user_events_schema).alias("data")
    ).select("data.*")
    
    # Windowed aggregations
    windowed_counts = parsed_df \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            window("timestamp", "5 minutes"),
            "event_type"
        ) \
        .count()
    
    # Write to console
    query = windowed_counts.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    return query

def process_sensor_data():
    """Process sensor data stream"""
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", TOPIC_SENSOR_DATA) \
        .load()
    
    # Parse JSON and apply schema
    parsed_df = df.select(
        from_json(col("value").cast("string"), sensor_data_schema).alias("data")
    ).select("data.*")
    
    # Calculate averages
    avg_metrics = parsed_df \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            window("timestamp", "5 minutes"),
            "sensor_id"
        ) \
        .agg(
            avg("temperature").alias("avg_temperature"),
            avg("humidity").alias("avg_humidity"),
            avg("pressure").alias("avg_pressure")
        )
    
    # Write to console
    query = avg_metrics.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    return query

def process_transactions():
    """Process transaction data stream"""
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", TOPIC_TRANSACTIONS) \
        .load()
    
    # Parse JSON and apply schema
    parsed_df = df.select(
        from_json(col("value").cast("string"), transactions_schema).alias("data")
    ).select("data.*")
    
    # Calculate transaction metrics
    transaction_metrics = parsed_df \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            window("timestamp", "5 minutes"),
            "currency"
        ) \
        .agg(
            count("*").alias("transaction_count"),
            sum("amount").alias("total_amount"),
            avg("amount").alias("avg_amount")
        )
    
    # Write to console
    query = transaction_metrics.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    return query

if __name__ == "__main__":
    print("Starting Spark Structured Streaming jobs...")
    
    # Start all streaming queries
    queries = []
    queries.append(process_user_events())
    queries.append(process_sensor_data())
    queries.append(process_transactions())
    
    # Wait for termination
    spark.streams.awaitAnyTermination() 