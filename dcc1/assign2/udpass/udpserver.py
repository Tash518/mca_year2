import socket

HOST = '127.0.0.1'
PORT = 8080

def start_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"[*] UDP Server listening on {HOST}:{PORT}...")
        while True:
            data, client_addr = server_socket.recvfrom(65535)
            print(f"[+] Received {len(data)} bytes from {client_addr}")
            response = f"ACK: Server received {len(data)} bytes.".encode('utf-8')
            server_socket.sendto(response, client_addr)

if __name__ == '__main__':
    start_udp_server()