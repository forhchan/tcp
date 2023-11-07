import socket

# HOST = '192.168.93.128'
HOST = '192.168.93.128'
PORT = 3333


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))    
while True:
    message = input("Leave a message : ")
    sock.send(f"{message}".encode('utf-8'))
    print(sock.recv(4096).decode('utf-8'))