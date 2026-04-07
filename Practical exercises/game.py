import socket

PORT = 8080
IP = "127.0.0.1"

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ls.bind((IP, PORT))

ls.listen()

print("Server configured!")

while True:
    print("Waiting for Clients...")

    try:
        (cs, client_ip_port) = ls.accept()

    except KeyboardInterrupt:
        print("\nServer stopped by the user")
        ls.close()
        exit()

    else:
        print("A client has connected to the server!")
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode().strip()

        parts = msg.split()
        if len(parts) > 0:
            command = parts[0]


                    response = str(s) + "\n"
                    print(response.strip())
                    cs.send(response.encode())
        cs.close()
