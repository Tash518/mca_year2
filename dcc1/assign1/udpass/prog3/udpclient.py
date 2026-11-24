
import socket
import os

CHUNK_SIZE = 1024
PORT = 12347

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", PORT)

client_socket.settimeout(5)

filename = input("Enter filename to request: ")

client_socket.sendto(filename.encode(), server_address)

try:
    data, server = client_socket.recvfrom(2048)

    if data.startswith(b"ERR:"):
        print(data.decode())

    elif data.startswith(b"OK|"):

    
        total_chunks = int(data.decode().split("|")[1])

        print("Total chunks expected:", total_chunks)

    
        chunks = {}

    
        while len(chunks) < total_chunks:

            packet, server = client_socket.recvfrom(CHUNK_SIZE + 64)

        
            header, chunk_data = packet.split(b"|", 2)[:2], packet.split(b"|", 2)[2]

        
            seq = int(header[0])
            received_total = int(header[1])

        
            if received_total == total_chunks and 0 <= seq < total_chunks:
                chunks[seq] = chunk_data

                print("Received chunk:", seq)

    
        file_data = b"".join(chunks[i] for i in range(total_chunks))

    
        output_filename = "received_" + os.path.basename(filename)

    
        with open(output_filename, "wb") as file:
            file.write(file_data)

        print("\nFile received successfully!")
        print("Saved as:", output_filename)
        print("Total bytes received:", len(file_data))

except socket.timeout:
    print("Transfer timed out. Some chunks may be missing.")

finally:
    client_socket.close()
