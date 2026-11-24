
import socket
import os
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 12346)
server_socket.bind(server_address)
print("UDP File Server is running...")
print("Waiting for client requests...")
while True:

    data, client_address = server_socket.recvfrom(1024)
    filename = data.decode().strip()
    print("Requested file:", filename)

    if os.path.isfile(filename):

        try:
    
            with open(filename, "rb") as file:
                content = file.read()
            if len(content) <= 1024:

        
                response = b"OK:" + content

            else:
                response = b"ERROR: File size exceeds 1024 bytes."

        except OSError:
            response = b"ERROR: Unable to read the file."

    else:
        response = b"ERROR: File not found."

    server_socket.sendto(response, client_address)

    print("Response sent to client.")
    print("--------------------------------")
