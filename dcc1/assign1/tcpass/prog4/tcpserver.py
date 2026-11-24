import socket
from datetime import datetime
import threading

HOST = "localhost"
PORT = 43854


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def get_date():
    return datetime.now().strftime("%Y/%m/%d")


def get_hostname():
    return socket.gethostname()


def process_command(command: str):
    command = command.strip()

    if command == "TIME":
        return "OK " + get_time(), False
    elif command == "DATE":
        return "OK " + get_date(), False
    elif command == "HOSTNAME":
        return "OK " + get_hostname(), False
    elif command.startswith("ECHO "):
        message = command[5:]
        return "OK " + message, False
    elif command == "QUIT":
        return "BYE", True
    else:
        return "ERROR, unknown command: " + command, False


def handle_client(client_socket, address):

    thread_name = threading.current_thread().name

    print(f"Client connected: " f"{address[0]}:{address[1]} " f"[{thread_name}]")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        command = data.decode()

        response, should_quit = process_command(command)
        client_socket.sendall(response.encode())
        if should_quit:
            break
    client_socket.close()
    print(f"\n client disconnected: {address[0]}:{address[1]}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"server listening on {HOST}:{PORT}")
        print("waiting for client...")
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    start_server()
