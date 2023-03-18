import matplotlib.pyplot as plt
from scapy.all import *
import time
from mrjob.job import MRJob

def plot_packet_length_vs_time(pkts):
    print("Hello")
    packet_lengths = [pkt.len for pkt in pkts]
    times = [pkt.time for pkt in pkts]
    
    plt.plot(times, packet_lengths, 'o')
    plt.xlabel('Time (s)')
    plt.ylabel('Packet Length (bytes)')
    plt.title('Packet Length vs Time')
    plt.show()

def capture_network_traffic(iface, duration):
    pkts = sniff(iface=iface, filter='tcp port 80', timeout=duration)
    return pkts


class NetworkTrafficCaptureJob(MRJob):
    def mapper(self, _, task):
        pkts = capture_network_traffic(iface="WiFi", duration=5)
        yield None, pkts
        
    def reducer(self, _, pkts):
        pkts = [pkt for pkts in pkts for pkt in pkts]
        plot_packet_length_vs_time(pkts)
        
if __name__ == '__main__':    
    NetworkTrafficCaptureJob().run()

