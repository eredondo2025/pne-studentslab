from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PORT = 8081

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # MAIN PAGE
        if path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = """
            <html>
                <head><title>SEQ2 server</title></head>
                <body>
                    <h1>SEQ2 server</h1>

                    <p>Access to the Server</p>
                    <hr>

                    <p>
                        Is the server alive?
                        <a href="/ping"><button>PING</button></a>
                    </p>

                    <hr>

                    <form action="/get" method="get">
                        <p>Get a Sequence. Select sequence number:</p>

                        <select name="seq_num">
                            <option value="0">0</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                        </select>

                        <button type="submit">GET</button>
                    </form>
                </body>
            </html>
            """
            self.wfile.write(html.encode())

        # PING
        elif path == "/ping":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = """
            <html>
                <body>
                    <h1>Server is alive!</h1>
                    <a href="/">Back</a>
                </body>
            </html>
            """
            self.wfile.write(html.encode())

        # GET SEQUENCE
        elif path == "/get" and "seq_num" in query:
            seq_num = int(query["seq_num"][0])

            sequences = [
                "ATCGACCCTGGAAAGTCAGTCTAGCTAGCTCTTTGCAA",
                "GATTACCAGCGGGACACTCATCGACCTGCTTTCGAGCA",
                "CCGTAAAGGGCTCGATCGTAGCTAGCTAGCTAGCTAGAC",
                "TTAACCGGGGCTAGCAAGCTCTAGGGCTACGCTAGCTAG",
                "AGCTAGCTCCGATCGAATCGATCGAGCGCATCTTAGGTC"
            ]

            if 0 <= seq_num < len(sequences):
                seq = ", ".join(map(str, sequences[seq_num]))

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                html = f"""
                <html>
                    <body>
                        <h1>Sequence {seq_num}</h1>
                        <p>{seq}</p>
                        <a href="/">Back</a>
                    </body>
                </html>
                """
                self.wfile.write(html.encode())
            else:
                self.send_error(404)

        # ERROR
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Not Found</h1>")


# RUN SERVER
if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), MyHandler)
    print(f"Running on http://localhost:{PORT}")
    server.serve_forever()