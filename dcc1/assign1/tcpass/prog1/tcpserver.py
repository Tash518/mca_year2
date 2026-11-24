import socket
import json

HOST = "localhost"
PORT = 43854


def analyse_string(text: str):
    strlen: int = len(text)
    vowels = set("aeiouAEIOU")
    vcount: int = 0
    dcount: int = 0
    ccount: int = 0
    for char in text:
        if char.isdigit():
            dcount += 1
        elif char.isalpha():
            if char in vowels:
                vcount += 1
            else:
                ccount+=1
    return (
        f"Analysis Results:\n"
        f"- Total Length: {strlen}\n"
        f"- Vowels: {vcount}\n"
        f"- Consonants: {ccount}\n"
        f"- Digits: {dcount}"
    )

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"server listening on {HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"connected on {addr}")
                data = conn.recv(1024).decode("utf-8")
                if not data: return
                print(f"decoded string: {data}")
                
                conn.sendall(analyse_string(data).encode("utf-8"))
if __name__ == "__main__":
    start_server()