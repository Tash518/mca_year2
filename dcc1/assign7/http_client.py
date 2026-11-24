import socket
import sys

if len(sys.argv) != 5:
    print("usage: python http_client.py <server> <port> <method> <path>")
    sys.exit(1)
    
server_host = sys.argv[1]
try:
    server_port = int(sys.argv[2])
    
    if not 1 <= server_port <= 65535:
        raise ValueError("Port number must be between 1 and 65535") 
except ValueError as e:
    print(f"Invalid port number: {e}")
    sys.exit(1)

method = sys.argv[3].upper()
resource_path = sys.argv[4]

if method not in ["GET", "POST"]:
    print("only get and out method accepted")
    sys.exit(1)

#creatin tcp socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.settimeout(10)
#connecting
try:
    client_socket.connect((server_host, server_port))
    
    print("connecton to server successful")
    print(f"server: {server_host}:{server_port}")
    
    #http req
    request = (
        f"{method} {resource_path} HTTP/1.0\r\n"
        f"Host: {server_host}\r\n"
        "\r\n"
    )
    #str to byte
    
    request_bytes = request.encode("ascii")
    
    print(f"request:\n{request}")
    
    #sending http req
    client_socket.sendall(request_bytes)
    print("request sent to server")
    
    #recieving
    response_chunks = []
    while True:
        chunk = client_socket.recv(4096)
        if chunk == b'':
            break
        response_chunks.append(chunk)
    
    response = b''.join(response_chunks).decode("utf-8", errors = "replace")
    
    print("\n===========HTTP response==========")
    print(response)
except socket.error as e:
    print(f"connection to server failed: {e}")
    sys.exit(1)

except OSError as e:
    print(f"connection to server failed: {e}")
    sys.exit(1)

finally:
    client_socket.close()
    print("socket closed")
    

