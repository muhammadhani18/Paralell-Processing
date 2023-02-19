import matplotlib.pyplot as plt
import socket
import json

def plot_packet_length_vs_time(data):
    packet_lengths = [pkt['length'] for pkt in data]
    times = [pkt['time'] for pkt in data]
    
    plt.plot(times, packet_lengths, 'o')
    plt.xlabel('Time (s)')
    plt.ylabel('Packet Length (bytes)')
    plt.title('Packet Length vs Time')
    plt.show()

def receive_data(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(2)  # allow up to 2 worker connections

    data = []
    for i in range(2):  # receive data from 2 workers
        client_socket, address = server_socket.accept()
        client_data = client_socket.recv(1024)
        client_data = json.loads(client_data.decode('utf-8'))
        data.extend(client_data)
    
    return data

if __name__ == '__main__':
    port = 12345
    data = receive_data(port)
    plot_packet_length_vs_time(data)
