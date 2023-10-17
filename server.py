import socket

# host = socket.gethostbyname(socket.gethostname())

HOST = '10.68.123.238'
PORT = 9091


count = 0

while True:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    server.listen(1)

    communication_socket, addr = server.accept()
    print(f"Connected to {addr}")
    message = communication_socket.recv(4096).decode('utf-8')
    print(f"Message from client is : {count} : {message}")
    if message:
        count += 1
    communication_socket.send(f"Got your message! Thank you!".encode('utf-8'))
    if message == "end":
        communication_socket.close()
        print(f"Connection with {addr} ended!")
    
    