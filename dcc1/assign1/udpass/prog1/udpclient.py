
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 12345)

while True:

    message = input("Enter DATE, TIME, DATETIME or EXIT: ")

    if message.upper() == "EXIT":
        break

    client_socket.sendto(message.encode(), server_address)

    data, server_address = client_socket.recvfrom(1024)

    print("Server response:", data.decode())

client_socket.close()
