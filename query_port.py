import socket

def get_server_port(server_address):
    query_port = 25565  # Minecraft Query Protocol default port

    try:
        # Connect to the server and send a Query request
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.connect((server_address, query_port))
            s.sendall(b'\xfe\xfd\x09\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00')
            data = s.recv(2048)

        # Parse the response to get the server port
        port_start = data.find(b'\x00\x00\x00\x00\x00\x00\x00\x00') + 8
        port_end = data.find(b'\x00', port_start)
        server_port = int(data[port_start:port_end])

        return server_port

    except Exception as e:
        print(f"Error querying Minecraft server: {e}")
        return None

# Example usage:
server_address = 'mc.hypixel.net'
current_port = get_server_port(server_address)
print(f"The current port of the Minecraft server {server_address} is {current_port}")
