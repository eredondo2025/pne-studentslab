import socket
import termcolor

# -- Step 1: Create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# -- Optional: This is to avoid problems if the port is in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# IP and PORT Configuration
PORT = 8080
IP = "212.128.255.91"

# -- Step 2: Bind
ls.bind((IP, PORT))

# -- Step 3: Configure to listen
ls.listen()

print("The server is configured!")

# <--- NEW LINE: Initialize the counter outside the loop
connection_count = 0
clients = []

while True:
    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()

    except KeyboardInterrupt:
        print("Server stopped by the user")
        ls.close()
        exit()

    else:
        clients.append(client_ip_port)
        # <--- NEW LINE: Increment the counter
        connection_count += 1

        # <--- NEW LINE: Print the counter and client info
        print(f"CONNECTION {connection_count}. Client IP,PORT: {client_ip_port}")

        # -- Read the client's message
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode()

        print("Message received:", end=" ")
        termcolor.cprint(msg, "green")

        # -- Send message back
        response = f"ECHO: {msg}"
        cs.send(response.encode())

        # -- Close data socket
        cs.close()

        if len(clients) == 5:
            break

print("The following clients has connected to the server:")
for i, client in enumerate(clients):
    print(f"Client {i}: {client}")