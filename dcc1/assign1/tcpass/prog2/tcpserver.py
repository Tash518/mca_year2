import socket
import os

HOST = "localhost"
PORT = 43854


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"server listening on {HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"connected on {addr}")
                filename = conn.recv(1024).decode("utf-8")
                if not filename:
                    continue
                print(f"received filename: {filename}")
                print(repr(filename))
                if os.path.isfile(filename):
                    with open(filename, "rb") as f:
                        conn.sendall(b"FOUND")
                        ack = conn.recv(1024)
                        while chunk := f.read(1024):
                            conn.sendall(chunk)
                else:
                    conn.sendall(b"NOT_FOUND")
                    print(f"{filename} not found")


if __name__ == "__main__":
    start_server()
