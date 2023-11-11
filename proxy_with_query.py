import socket
import threading

def get_remote_port(server_ip):
    query_port = 25565  # Minecraft Query Protocol default port

    try:
        # Connect to the server and send a Query request
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.connect((server_ip, query_port))
            s.sendall(b'\xfe\xfd\x09\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00')
            data = s.recv(2048)

        # Parse the response to get the server port
        port_start = data.find(b'\x00\x00\x00\x00\x00\x00\x00\x00') + 8
        port_end = data.find(b'\x00', port_start)
        server_port = int(data[port_start:port_end])

        return server_port

    except Exception as e:
        print(f"Error querying server: {e}")
        return None

def handle_client(client_socket, remote_host):
    remote_port = get_remote_port()
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    def forward(src, dst):
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)

    client_to_remote = threading.Thread(target=forward, args=(client_socket, remote_socket))
    remote_to_client = threading.Thread(target=forward, args=(remote_socket, client_socket))

    client_to_remote.start()
    remote_to_client.start()

def start_proxy_server(local_port, remote_host):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', local_port))
    server.listen(5)
    print(f'Proxy server listening on port {local_port}')

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        proxy_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host))
        proxy_thread.start()

if __name__ == '__main__':
    # 프록시 서버 설정
    local_port = 8888  # 로컬에서 접속할 포트
    remote_host = 'game-server-address.com'  # 실제 게임 서버 주소

    # 프록시 서버 시작
    start_proxy_server(local_port, remote_host)