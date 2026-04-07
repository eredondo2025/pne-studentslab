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

        try:
            resource = req_line.split()[1]
        except IndexError:
            resource = "/"

        if resource == "/":
            file_to_open = "html/index.html"
            status_line = "HTTP/1.1 200 OK\n"
        elif resource == "/info/A":
            file_to_open = "html/info/A.html"
            status_line = "HTTP/1.1 200 OK\n"
        elif resource == "/info/C":
            file_to_open = "html/info/C.html"
            status_line = "HTTP/1.1 200 OK\n"
        elif resource == "/info/G":
            file_to_open = "html/info/G.html"
            status_line = "HTTP/1.1 200 OK\n"
        elif resource == "/info/T":
            file_to_open = "html/info/T.html"
            status_line = "HTTP/1.1 200 OK\n"
        else:
            file_to_open = "html/error.html"
            status_line = "HTTP/1.1 404 Not Found\n"

        try:
            with open(file_to_open, "r", encoding="utf-8") as f:
                body = f.read()
        except FileNotFoundError:
            body = "<h1>Error: File not found</h1>"
            status_line = "HTTP/1.1 404 Not Found\n"

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