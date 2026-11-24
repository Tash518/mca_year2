import socket
import os
import struct

CHUNK_SIZE = 1024
PORT = 12347

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", PORT)
server_socket.bind(server_address)

print("UDP Chunk File Server started...")
print("Waiting for client requests...")

while True:
    try:
        data, client_address = server_socket.recvfrom(1024)

    except ConnectionResetError:
        print("UDP connection reset notification received. Continuing...")
        continue

    data, client_address = server_socket.recvfrom(1024)

    filename = data.decode().strip()

    print("\nRequested file:", filename)

    if not os.path.isfile(filename):
        server_socket.sendto(b"ERR: File not found.", client_address)
        continue

    try:

        with open(filename, "rb") as file:
            file_data = file.read()

        total_chunks = (len(file_data) + CHUNK_SIZE - 1) // CHUNK_SIZE

        response = b"OK:" + struct.pack("!I", total_chunks)

        server_socket.sendto(response, client_address)

        print("File size:", len(file_data), "bytes")
        print("Total chunks:", total_chunks)

        for seq in range(total_chunks):

            start = seq * CHUNK_SIZE
            end = start + CHUNK_SIZE

            chunk = file_data[start:end]

            header = struct.pack("!II", seq, total_chunks)

            packet = header + chunk

            server_socket.sendto(packet, client_address)

            print("Sent chunk:", seq)

        print("File transfer completed.")
        print("--------------------------------")

    except OSError:
        server_socket.sendto(b"ERR: Unable to read file.", client_address)
