import socket

HOST = '127.0.0.1'  # Change if connecting remotely
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server. Listening for messages...\n")

    while True:
        data = s.recv(1024)
        if not data:
            break  # Stop if connection is closed
        print(data.decode('utf-8'), end="") 