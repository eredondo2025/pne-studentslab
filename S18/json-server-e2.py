import http.server
import socketserver
from pathlib import Path

PORT = 8080

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if the requested resource is /listusers
        if self.path == '/listusers':
            try:
                # Read the content of the JSON file
                json_content = Path("people-e1.json").read_text()

                # Send 200 OK response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # Write the JSON content to the response body
                self.wfile.write(bytes(json_content, "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            # For any other path, return 404
            self.send_error(404, "Resource not found")

# Start the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()