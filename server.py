import socket

# host = socket.gethostbyname(socket.gethostname())

# HOST = '45.77.11.68'
# PORT = 3128

HOST = '192.168.93.1'
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

count = 1
print(f"Waiting for response from client")

while True:    
    communication_socket, addr = server.accept()
    print(f"Connected to {addr}")
    
    while True:
        
        message = communication_socket.recv(4096).decode('utf-8')
        print(f"Message from client is : {count} : {message}")
        
        if not message:
            break
        if message == "end":
            break
        communication_socket.send(f"Got your message! Thank you!".encode('utf-8'))
        count += 1
    communication_socket.close()
    print(f"Connection with {addr} ended!")
    


