import socket
import termcolor

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

PORT = 8080
IP = "127.0.0.1"

SEQUENCES = [
    "ACCTCCTCTCCAGC",
    "CCCTAGCCTGACTC",
    "CAAGGTCCCCTTCT",
    "GATTACAATTACCA",
    "ACTGCTGGACTCTG"
]

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ls.bind((IP, PORT))

ls.listen()

print("SEQ Server configured!")

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

            if command == "PING":
                termcolor.cprint("PING command!", "green")
                response = "OK!\n"
                print(response.strip())
                cs.send(response.encode())

            elif command == "GET":
                if len(parts) > 1:
                    termcolor.cprint("GET", "green")
                    index = int(parts[1])
                    response = SEQUENCES[index] + "\n"
                    print(response.strip())
                    cs.send(response.encode())

        cs.close()

