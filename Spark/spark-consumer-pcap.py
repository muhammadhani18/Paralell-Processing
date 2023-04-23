from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import time

#the name to the topic that the consumer needs to receive messages from- same topic that the producer feeds the messages to. We also set the kafka server and port and start a Spark session.

kafka_topic_name = "pkttest_pcap"
kafka_bootstrap_servers = 'localhost:9092'


spark = SparkSession.builder.appName("Structured Streaming Pkt").master("local[*]").getOrCreate()

spark.sparkContext.setLogLevel("Error")

pkt_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", kafka_bootstrap_servers).option("subscribe", kafka_topic_name).load()

pkt_df1 = pkt_df.selectExpr("CAST(value as String)", "timestamp")

query = pkt_df.writeStream.trigger(processingTime='2 seconds').outputMode("update").format("console").start()

query.awaitTermination()






#sparkDF=spark.createDataFrame(pkt_df)

#sparkDF.printSchema()

#sparkDF.show()

#construt a streaming dataframe that reads from topic


# pkt_schema_string = "count INT, scr_ip STRING, dst_ip STRING, proto INT, sport STRING, dport STRING"

# pkt_df2 = pkt_df1.select(from_csv(col("value"),pkt_schema_string).alias("pkt"), "timestamp")

# pkt_df3 = pkt_df2.select("pkt.*", "timestamp")


