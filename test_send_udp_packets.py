import time
import socket
import pickle

UDP_IP = "192.168.1.255"
UDP_PORT = 5005
MESSAGE = (1, 3.32)

print(f"UDP target IP: {UDP_IP}")
print(f"UDP target port: {UDP_PORT}")
print(f"message: {MESSAGE}")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while 1:
        sock.sendto(pickle.dumps(MESSAGE), (UDP_IP, UDP_PORT))
        time.sleep(1)