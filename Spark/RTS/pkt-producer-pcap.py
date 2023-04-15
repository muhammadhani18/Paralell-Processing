from time import sleep
from kafka import KafkaProducer
from struct import *
#to read packets header files
import MyScapyExtract as myscap
import time
import nfstream
from nfstream import *
import csv
import pandas as pd
import json

#create the kafka producer which connects to kafka server at port 9092
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

print('Created Producer\n')

streamer = NFStreamer(source='./sample1.pcap')

df = streamer.to_pandas(columns_to_anonymize=[])

print(df)

overlap = ""
oldtime = time.time()

for i in df.iterrows():

    if time.time() - oldtime >= 2: # 2 seconds
        producer.send('pkttest_pcap',overlap)
        oldtime = time.time()


    data = json.dumps(i, default=str).encode('utf-8')
#    print(data)
    producer.send("pttest_pcap",data)
    overlap = data