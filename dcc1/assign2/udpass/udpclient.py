import socket

HOST = '127.0.0.1'
PORT = 8089

def start_udp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        print(f"[*] UDP Client started. Target: {HOST}:{PORT}")
        print("Choose message size:")
        print("  1. Short message (~30 bytes)")
        print("  2. Medium message (512 bytes)")
        print("  3. Large message (2048 bytes)")
        print("  q. Quit")
        
        while True:
            choice = input("\nEnter option (1/2/3/q): ").strip().lower()
            if choice == '1':
                msg = b"Hello from UDP client instance!"
            elif choice == '2':
                msg = b"B" * 512
            elif choice == '3':
                msg = b"C" * 2048
            elif choice == 'q':
                break
            else:
                print("Invalid choice.")
                continue
                
            client_socket.sendto(msg, (HOST, PORT))
            print(f"[+] Sent {len(msg)} bytes to server.")
            
            try:
                client_socket.settimeout(2.0)
                data, server_addr = client_socket.recvfrom(65535)
                print(f"[+] Received reply: {data.decode('utf-8', errors='ignore')}")
            except socket.timeout:
                print("[-] Request timed out (No response from server).")

if __name__ == '__main__':
    start_udp_client()