import socket
from scapy.all import *
import time

def capture_network_traffic(iface, duration):
    pkts = sniff(iface=iface, filter='tcp port 80', timeout=duration)
    return pkts

def send_data_to_master(master_ip, master_port, pkts):
    data = [str(pkt.len) + ',' + str(pkt.time) for pkt in pkts]
    data = '\n'.join(data)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((master_ip, master_port))
        s.sendall(data.encode('utf-8'))

if __name__ == '__main__':
    iface = 'eth0'
    duration = 5  # duration in seconds
    master_ip = '0.0.0.0'
    master_port = 12345
    
    pkts = capture_network_traffic(iface=iface, duration=duration)
    send_data_to_master(master_ip, master_port, pkts)
