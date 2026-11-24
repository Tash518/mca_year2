
import socket
from datetime import datetime

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 12345)
server_socket.bind(server_address)

print("UDP Date and Time Server is running...")
print("Waiting for client requests...")

while True:

    data, client_address = server_socket.recvfrom(1024)

    request = data.decode().strip().upper()

    print("Request received:", request)
    print("Client address:", client_address)

    now = datetime.now()

    if request == "DATE":
        response = now.strftime("%Y-%m-%d")

    elif request == "TIME":
        response = now.strftime("%H:%M:%S")

    elif request == "DATETIME":
        response = now.strftime("%Y-%m-%d %H:%M:%S")

    else:
        response = "Invalid request! Use DATE, TIME or DATETIME."

    server_socket.sendto(response.encode(), client_address)

    print("Response sent:", response)
    print("--------------------------------")
