from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pymongo import MongoClient

# MongoDB connection details
mongo_uri = "mongodb+srv://mhani:Deviljin1@batchdata.niq660y.mongodb.net/?retryWrites=true&w=majority"
mongo_db = "spark"
mongo_collection = "Spark"

# Create Spark session
spark = SparkSession.builder.appName("StreamToMongoDB").getOrCreate()

# Create Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "pkttest_pcap") \
    .load()

# Convert Kafka value column to string
df = df.selectExpr("CAST(value AS STRING)", "timestamp")

pkt_schema_string = "count INT, scr_ip STRING, dst_ip STRING, proto INT, sport STRING, dport STRING"

# Parse JSON string into columns
#df = df.select(from_json(col("value"), "col1 INT, col2 STRING").alias("data"))

df = df.select(from_json(col("value"),pkt_schema_string).alias("pkt"), "timestamp")

# Extract columns from data struct
df = df.select("pkt.count", "pkt.src_ip","pkt.dst_ip","pkt.dport")

# Write data to MongoDB
df.writeStream \
    .foreachBatch(lambda batch_df, batch_id: 
        batch_df.write \
            .format("mongo") \
            .option("uri", mongo_uri) \
            .option("database", mongo_db) \
            .option("collection", mongo_collection) \
            .mode("append") \
            .save()
    ) \
    .start() \
    .awaitTermination()
