import socket

HOST = '10.68.108.93'

PORT = 9091

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))    
    message = input("Leave a message : ")
    sock.send(f"{message}".encode('utf-8'))
    print(sock.recv(4096).decode('utf-8'))