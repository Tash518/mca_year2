
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 12348)
while True:
    hostname = input("Enter hostname (or EXIT to quit): ")

    if hostname.upper() == "EXIT":
        print("Client closing...")
        break


    client_socket.sendto(hostname.encode(), server_address)


    data, server = client_socket.recvfrom(1024)


    response = data.decode()

    print("Server response:", response)

client_socket.close()
