import http.server
import socketserver
import termcolor
import os
from pathlib import Path

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

# Class with our Handler. It is derived from BaseHTTPRequestHandler
# It means that our class inherits all its methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # Define the root folder where the files will be stored
        root_folder = Path(os.getcwd())  # Get current working directory

        # Check if the requested path is the root or a valid file
        requested_path = root_folder / self.path.lstrip("/")  # Remove the leading slash if exists

        try:
            # Check if the file exists
            if requested_path.exists() and requested_path.is_file():
                # Send a 200 OK response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Open the requested file and read its content
                with open(requested_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                # If the file doesn't exist, serve the error page
                self.serve_error_page()
        except FileNotFoundError:
            # Catch FileNotFoundError and serve the error page
            self.serve_error_page()

    def serve_error_page(self):
        # Send a 404 error page
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Open and send the error.html file
        error_file = Path(os.getcwd()) / "error.html"
        with open(error_file, 'rb') as file:
            self.wfile.write(file.read())

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