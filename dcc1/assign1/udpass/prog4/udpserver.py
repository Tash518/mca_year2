
import socket

name_table = {
    "server1": "192.168.1.10",
    "server2": "192.168.1.20",
    "server3": "192.168.1.30",
    "server4": "192.168.1.40"
}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("127.0.0.1", 12348))

print("UDP Name Server is running...")

while True:


    data, client_address = server_socket.recvfrom(1024)


    hostname = data.decode().strip()

    print("Received hostname:", hostname)


    if hostname in name_table:
        response = name_table[hostname]
    else:
        response = "NOT FOUND"


    server_socket.sendto(response.encode(), client_address)

    print("Sent response:", response)
