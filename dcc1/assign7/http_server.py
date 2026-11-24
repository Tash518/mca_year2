import socket
import sys

if len(sys.argv) != 2:
    print("usage: http_server.py <port>")
    sys.exit(1)

try:
    server_port = int(sys.argv[1])
    
    if not 1 <= server_port <= 65535:
        raise ValueError("Port number must be between 1 and 65535")
except ValueError as e:
    print("INVALID PORT NUMBER")
    sys.exit(1)

#ipv4 socket

server_soccket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_soccket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_soccket.bind(("0.0.0.0", server_port))
    server_soccket.listen(5)

    print(f"HTTP server listening on port {server_port}...")

    while True:
        client_socket, client_address = server_soccket.accept()
        print("\nclient connected", client_address)
        
        #closing
        client_socket.close()
except KeyboardInterrupt:
    print("\nServer shutting down...")
    server_soccket.close()
    sys.exit(0)
except OSError as e:
    print("server error", e)
finally:
    server_soccket.close()