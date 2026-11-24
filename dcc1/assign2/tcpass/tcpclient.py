import socket
import time

HOST = '127.0.0.1'
PORT = 8080

def start_client():
    payload = b"A" * ( 1024**2 *1)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"[*] Connecting to {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Press 'm' to send 1 MB.") 
        print("Press 'q' to quit.")
        while True:
            opt = input("\nEnter m or q:").strip().lower()
            if opt == 'm':
                client_socket.sendall(payload)
                time.sleep(1)
            elif opt == 'q':
                print("[*] Quitting...")
                return
            else:
                print("Invalid input. Please enter 'm' or 'q'.")        
        
    print("[+] Data transfer complete. Closing connection.")

if __name__ == '__main__':
    start_client()