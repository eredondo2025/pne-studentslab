import socket
import termcolor


# -- Server network parameters
IP = "127.0.0.1"
PORT = 8080


def process_client(s):
    # -- Receive the request message
    req_raw = s.recv(2000)
    req = req_raw.decode()

    print("Message FROM CLIENT: ")

    # -- Split the request messages into lines
    lines = req.split('\n')
    if len(lines) > 0:
        req_line = lines[0]
        print(f"Request line: {req_line}")

        if "/info/A" in req_line:
            with open("A.html", "r", encoding="utf-8") as f:
                body = f.read()
            status_line = "HTTP/1.1 200 OK\n"

        elif "/info/C" in req_line:
            with open("C.html", "r", encoding="utf-8") as f:
                body = f.read()
            status_line = "HTTP/1.1 200 OK\n"

        elif "/info/G" in req_line:
            with open("G.html", "r", encoding="utf-8") as f:
                body = f.read()
            status_line = "HTTP/1.1 200 OK\n"

        elif "/info/T" in req_line:
            with open("T.html", "r", encoding="utf-8") as f:
                body = f.read()
            status_line = "HTTP/1.1 200 OK\n"

        else:
            with open("T.html", "r", encoding="utf-8") as f:
                body = f.read()
            status_line = "HTTP/1.1 200 OK\n"

        header = "Content-Type: text/html\n"
        header += f"Content-Length: {len(body)}\n"

        response_msg = status_line + header + "\n" + body
        cs.send(response_msg.encode())


# -------------- MAIN PROGRAM
# ------ Configure the server
# -- Listening socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Setup up the socket's IP and PORT
ls.bind((IP, PORT))

# -- Become a listening socket
ls.listen()

print("web server configured!")

# --- MAIN LOOP
while True:
    print("Waiting for clients....")
    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server stopped!")
        ls.close()
        exit()
    else:

        # Service the client
        process_client(cs)

        # -- Close the socket
        cs.close()