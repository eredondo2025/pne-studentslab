import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path

PORT = 8081

BASE_DIR = Path(__file__).parent


class EchoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("PATH RECEIVED:", self.path)

        url_path = urlparse(self.path)
        path = url_path.path

        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file_path = BASE_DIR / "html/form-2.html"
            print("LOADING:", file_path)  # DEBUG

            content = file_path.read_text()
            self.wfile.write(content.encode("utf8"))

        elif path.startswith("/echo"):
            arguments = parse_qs(url_path.query)

            message = arguments.get('msg', [''])[0]

            caps = arguments.get('caps')
            if caps is not None:
                message = message.upper()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            response = f"<html><body><h1>Echo Response</h1>"
            response += f"<p>You said: {message}</p>"
            response += f'<a href="/">Back to the form</a></body></html>'

            self.wfile.write(response.encode("utf8"))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file_path = BASE_DIR / "html/error.html"
            print("LOADING ERROR:", file_path)

            content = file_path.read_text()
            self.wfile.write(content.encode("utf8"))


with socketserver.TCPServer(("", PORT), EchoHandler) as httpd:
    print(f"Server running at {PORT}")
    httpd.serve_forever()