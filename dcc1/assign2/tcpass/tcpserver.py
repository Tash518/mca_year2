import socket
import time

HOST = '127.0.0.1'
PORT = 8080
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[*] listening on {HOST}:{PORT}....")
        conn, addr = server_socket.accept()
        with conn:
            print(f"[+] connected by {addr}")
            total_bytes = 0
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                total_bytes += len(data)
                print(f"[+] Received {len(data)} bytes of data from {addr}. Total received: {total_bytes} bytes.")
            print(f"[+] Received {total_bytes} bytes of data from {addr}.")

if __name__ == '__main__':
    start_server()