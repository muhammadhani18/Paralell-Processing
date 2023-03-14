from nfstream import NFStreamer

streamer = NFStreamer(source='./DNS_Flood.pcap')

for flow in streamer:
    print(flow)
    
    