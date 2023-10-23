import socket
from threading import Thread
import os


def parse(data, port, origin):
    print(f"[{origin} ({port})] {data.encode('hex')}")

class Proxy2Server(Thread):
    def __init__(self, host, port):
        self.game = None # game clinet socket not known yet
        super().__init__()
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        
    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                # try:
                #     reload(parse)
                #     parse(data, self.port, 'server')
                # except Exception as e:
                #     print(f"server[{self.port}]", e)
                # parse(data, self.port, 'server')
                print(f"[{self.port} -> {data[:100].encode('hex')}]")
                # forward to client
                self.game.sendall(data)

class Game2Proxy(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server = None # read server socket not known yet
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        self.game, addr = sock.accept()
    
    def run(self):
        while True:
            data = self.game.recv(4096)
            if data:
                # try:
                #     # reload(parse)
                #     parse(data, self.port, 'client')
                # except Exception as e:
                #     print(f"server[{self.port}]", e)
                # parse(data, self.port, 'client')
                print(f"[{self.port} -> {data[:100].encode('hex')}]")
                # forward to server
                self.server.sendall(data)

class Proxy(Thread):
    def __init__(self, from_host, to_host, port):
        super().__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
        
    def run(self):
        while True:
            print(f"[proxy({self.port})] setting up")
            self.g2p = Game2Proxy(self.from_host, self.port)
            self.p2s = Proxy2Server(self.to_host, self.port)
            print(f"[proxy({self.port})] connection established")
            self.g2p.server = self.p2s.server
            self.p2s.game = self.g2p.game
            
            self.g2p.start()
            self.p2s.start()


master_server = Proxy('0.0.0.0', '192.168.178.54', 3333)  # real server ip 192.168...
master_server.start()

for port in range(3000, 3006):
    _game_server = Proxy('0.0.0.0', '192.168.178.54', port )
    _game_server.start()


while True:
    try:
        cmd = raw_input("$")
        if cmd[:4] == 'quit':
            os._exit()
    except Exception as e:
        print(e)