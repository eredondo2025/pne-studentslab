import http.server
import socketserver
import termcolor
import os

# Define the Server's port
PORT = 8081

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is derived from BaseHTTPRequestHandler
# It means that our class inherits all its methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # Check if the requested path is the root or the index page
        if self.path == "/" or self.path == "/index.html":
            # Serve index.html
            self.path = "/index.html"
        else:
            # Serve error.html for any other paths
            self.path = "/error.html"

        # Construct the full file path
        file_path = os.getcwd() + self.path

        # Check if the requested file exists
        if os.path.exists(file_path):
            # Send a 200 OK response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Open the requested file and read its content
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            # If the file doesn't exist, send a 404 error
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Send a simple error message
            self.wfile.write(b"404 Not Found")


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at PORT {PORT}")

    # -- Main loop: Attend the client. Whenever there is a new
    # -- client, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()