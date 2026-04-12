import http.server
import socketserver
import os
from pathlib import Path

# Define the Server's port
PORT = 8081

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is derived from BaseHTTPRequestHandler
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # Define the root folder for the HTML files
        root_folder = Path(os.getcwd()) / "P05" / "html"

        # Handle the request for the main page
        if self.path == "/":
            self.path = "/index.html"

        # Define the file path
        file_path = root_folder / self.path.lstrip("/")

        # Check if the file exists
        if file_path.exists() and file_path.is_file():
            # Send a 200 OK response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Open the requested file and write it to the response
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            # If the file doesn't exist, serve the error page
            self.serve_error_page()

    def serve_error_page(self):
        # Send a 404 error response
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Open and serve error.html
        error_file = Path(os.getcwd()) / "P05" / "html" / "error.html"
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