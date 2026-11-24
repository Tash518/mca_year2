
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 12346)

while True:


    filename = input("Enter filename (or EXIT to quit): ")

    if filename.upper() == "EXIT":
        break


    client_socket.sendto(filename.encode(), server_address)


    data, server = client_socket.recvfrom(2048)


    if data.startswith(b"OK:"):

    
        content = data[3:]

        print("\nFile content:")
        print(content.decode("utf-8", errors="replace"))

    else:

    
        print("\nServer response:", data.decode())

    print("--------------------------------")

client_socket.close()
