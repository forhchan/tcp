import socket

HOST = '192.168.0.116'

PORT = 8000

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))    
    message = input("Leave a message : ")
    sock.send(f"{message}".encode('utf-8'))
    print(sock.recv(4096).decode('utf-8'))