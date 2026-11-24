import socket

HOST = "localhost"
PORT = 43854

def start_client():
    user_input = input("enter a strin: ")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST,PORT))
        client_socket.sendall(user_input.encode("utf-8"))

        res = client_socket.recv(1024).decode("utf-8")
        print(res)
if __name__ == "__main__":
    start_client()