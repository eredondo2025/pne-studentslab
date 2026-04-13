import http.server
import socketserver
import os
from pathlib import Path

# -- Server port definition
PORT = 8081

# -- Prevent "Port already in use" error
socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # 1. Define the base directory where this script is located
        # Using __file__ avoids duplicated path errors (e.g., P05/P05)
        base_dir = Path(__file__).parent
        root_folder = base_dir / "html"

        # 2. Handle the requested path
        if self.path == "/" or self.path == "":
            relative_path = "index.html"
        else:
            # Remove the leading slash so Path join works correctly
            relative_path = self.path.lstrip("/")

        # 3. Build the full path to the requested file
        file_path = root_folder / relative_path

        # 4. Check if the file exists and serve it
        if file_path.exists() and file_path.is_file():
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            # If the file does not exist, serve the custom error page
            self.serve_error_page(root_folder)

    def serve_error_page(self, root_folder):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Look for error.html inside the html folder
        error_file = root_folder / "error.html"

        if error_file.exists():
            with open(error_file, 'rb') as file:
                self.wfile.write(file.read())
        else:
            # Fallback response if error.html is missing
            self.wfile.write(b"<html><body><h1>Error 404: File not found</h1></body></html>")


# ------------------------
# - Server MAIN program
# ------------------------
Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at PORT {PORT}")
    # Print the path to verify the server is looking in the correct folder
    print(f"Root folder: {Path(__file__).parent / 'html'}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()