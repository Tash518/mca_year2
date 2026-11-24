import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

print(f"TCP Server listening on {SERVER_IP}:{SERVER_PORT}...")

try:
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        conn.close()
except KeyboardInterrupt:
    print("\nServer shutting down.")
finally:
    server_socket.close()