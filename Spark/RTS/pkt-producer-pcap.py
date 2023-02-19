#sources packet data by reading a pcap file and streams it to Kafka.

from time import sleep
from struct import *
from kafka import KafkaProducer

#to read packets header files
import MyScapyExtract as myscap


#create the kafka producer which connects to kafka server at port 9092
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: x.encode('utf-8'))

print('Created Producer\n')

file0 = 'TCP_Attack.pcap'
#load pcap files and extract headers fields 
packets = myscap.scapy_read_packets(file0)

#it will be a dictionary of elements
datalst = myscap.parse_scapy_packets(packets)


print(datalst[0:2])
print(len(packets))

count = 1

#iterates through each packet, takes only IP packets ( ethertype decimal 2048 corresponds to 0x0800 ) and extracts the 5-tuple ( Source IP address, Dest IP address, Protocol- 17 if UDP or 6 if TCP , Source Port, Destination Port). Then it packs this 5-tuple data in to a message along with the count of the packet and sends it to Kafka using send() method of KafkaProducer.

for i in range (len(datalst)):
    pkt = datalst[i]
    
    if(pkt['etype'] == '2048'):
        isrc = pkt['isrc']
        idst = pkt['idst']
        iproto = pkt['iproto']
        
        if iproto == 17:
            sport = pkt['utsport']
            dport = pkt['utdport']
        else:
            sport = pkt['tsport']
            dport = pkt['tdport']
    msg = str(count) + ',' + str(isrc) + ',' + str(idst) + ',' + str(iproto) + ',' + str(sport) + ',' + str(dport)
    
    print(msg)
    count+=1         

#pkttest_pcap is the topic the producer chooses to append the message in Kafka
    producer.send('pkttest_pcap',msg)
    sleep(1)







