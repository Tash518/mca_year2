import socket

HOST = "localhost"
PORT = 43854

def start_client():
    user_input = input("enter a strin: ")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST,PORT))
        client_socket.sendall(user_input.encode("utf-8"))

        stat = client_socket.recv(1024).decode("utf-8")
        if stat == "FOUND":
            print("FILE FOUND ON SERVER")
            client_socket.sendall(b"ACK")
            savename = f"downloaded_{user_input}"
            with open(savename,"wb") as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data: break
                    f.write(data)
            print("file saved")
        else:
            print("file not found")
            
if __name__ == "__main__":
    start_client()