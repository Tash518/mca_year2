import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print(f"UDP Server listening on {SERVER_IP}:{SERVER_PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received message from {addr}: {data.decode('utf-8', errors='ignore')}")
        # Optionally echo back to trigger an app-level UDP response
        sock.sendto(b"Hello from UDP Server", addr)
except KeyboardInterrupt:
    print("\nServer shutting down.")
finally:
    sock.close()