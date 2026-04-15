import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path

PORT = 8080


class EchoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("PATH RECEIVED:", self.path)
        url_path = urlparse(self.path)
        path = url_path.path

        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            content = Path("html/form-e1.html").read_text()
            self.wfile.write(bytes(content, "utf8"))

        elif path == "/echo":
            # 1. First, we extract the message from the URL
            arguments = parse_qs(url_path.query)
            message = arguments.get('msg', [''])[0]

            # 2. We send the success headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # This part generates the "blank page" with the message and the link
            response = f"<html><body><h1>Echo Response</h1>"
            response += f"<p>You said: {message}</p>"
            response += f'<a href="/">Back to the form</a></body></html>'

            # 3. Finally, we send the generated HTML to the browser
            self.wfile.write(bytes(response, "utf8"))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            content = Path("html/error.html").read_text()
            self.wfile.write(bytes(content, "utf8"))


with socketserver.TCPServer(("", PORT), EchoHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()