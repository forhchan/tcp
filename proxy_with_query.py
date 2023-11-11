import socket
import threading

def get_remote_port():
    # 여기에서 게임 서버의 현재 포트를 동적으로 가져오는 로직을 구현합니다.
    # 예를 들어, 게임 서버에 쿼리를 보내거나 다른 방법을 사용하여 현재 포트를 얻을 수 있습니다.
    # 이 예제에서는 임의의 값을 반환하도록 하겠습니다.
    return 12345

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