import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# -- Server port definition
PORT = 8081

# -- Prevent "Port already in use" error
socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # 1. Define the base directory where this script is located
        base_dir = Path(__file__).parent
        root_folder = base_dir / "html"

        # 2. Handle /ping and /get endpoints
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if path == "/" or path == "":
            relative_path = "index.html"
        elif path == "/ping":
            self.serve_ping_page(root_folder)
            return
        elif path == "/get" and "seq_num" in query:
            seq_num = int(query["seq_num"][0])  # Get the sequence number from the URL query
            self.serve_sequence(root_folder, seq_num)
            return
        else:
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

    def serve_ping_page(self, root_folder):
        # Handle the '/ping' endpoint
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = """
        <html>
            <head><title>Ping</title></head>
            <body>
                <h1>Server is alive!</h1>
                <a href="/">Go back to main page</a>
            </body>
        </html>
        """
        self.wfile.write(response.encode())

    def serve_sequence(self, root_folder, seq_num):
        # Handle the '/get' endpoint, returning the selected sequence
        sequences = [
            [1, 1, 1],                # Sequence 0
            [1, 2, 3, 5, 8],          # Sequence 1
            [2, 4, 6, 8, 10],         # Sequence 2
            [1, 4, 9, 16, 25],        # Sequence 3
            [1, 3, 6, 10, 15]         # Sequence 4
        ]

        # Check if seq_num is valid
        if 0 <= seq_num < len(sequences):
            sequence = sequences[seq_num]
            sequence_str = ", ".join(map(str, sequence))

            # Create response with the sequence
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            response = f"""
            <html>
                <head><title>Sequence {seq_num}</title></head>
                <body>
                    <h1>Sequence {seq_num}:</h1>
                    <p>{sequence_str}</p>
                    <a href="/">Go back to main page</a>
                </body>
            </html>
            """
            self.wfile.write(response.encode())
        else:
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

# - Server MAIN program
Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at PORT {PORT}")
    print(f"Root folder: {Path(__file__).parent / 'html'}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()