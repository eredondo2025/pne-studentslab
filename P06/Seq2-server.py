from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

PORT = 8081

BASE_DIR = os.path.dirname(__file__)
SEQUENCES_FOLDER = os.path.join(BASE_DIR, "..", "sequences")


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

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

                    <hr>

                    <form action="/gene" method="get">
                        <p>Get a Gene. Select the name:</p>
                        <select name="gene_name">
                            <option value="U5">U5</option>
                            <option value="ADA">ADA</option>
                            <option value="FRAT1">FRAT1</option>
                            <option value="RNU6_269P">RNU6_269P</option>
                            <option value="FXN">FXN</option>
                        </select>
                        <button type="submit">GENE</button>
                    </form>

                    <hr>

                    <form action="/operation" method="get">
                        <p>Write a sequence: <input type="text" name="seq" required></p>
                        <p>Select operation: 
                            <input type="radio" name="op" value="info" checked> Info
                            <input type="radio" name="op" value="comp"> Comp
                            <input type="radio" name="op" value="rev"> Rev
                        </p>
                        <p>Perform operation: <button type="submit">OPERATE!</button></p>
                    </form>
                    <hr>

                </body>
            </html>
            """
            self.wfile.write(html.encode())

        # --- PING ---
        elif path == "/ping":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = "<html><body><h1>Server is alive!</h1><a href='/'>Back</a></body></html>"
            self.wfile.write(html.encode())

        # --- GET SEQUENCE ---
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
                seq = sequences[seq_num]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = f"<html><body><h1>Sequence {seq_num}</h1><p>{seq}</p><a href='/'>Back</a></body></html>"
                self.wfile.write(html.encode())
            else:
                self.send_error(404)

        # --- GENE ---
        elif path == "/gene" and "gene_name" in query:
            gene_name = query["gene_name"][0]
            file_path = os.path.join(SEQUENCES_FOLDER, gene_name + ".txt")

            try:
                with open(file_path, "r") as f:
                    gene_seq = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = f"<html><body><h1>Gene: {gene_name}</h1><pre>{gene_seq}</pre><a href='/'>Back</a></body></html>"
                self.wfile.write(html.encode())
            except FileNotFoundError:
                self.send_error(404, f"Gene {gene_name} not found")

        elif path == "/operation" and "seq" in query and "op" in query:
            sequence = query["seq"][0].upper()
            op = query["op"][0]

            result_body = f"<h2>Sequence</h2><p>{sequence}</p><h2>Operation:</h2><p>{op}</p><h2>Result:</h2>"

            if op == "info":
                length = len(sequence)
                a = sequence.count('A')
                c = sequence.count('C')
                g = sequence.count('G')
                t = sequence.count('T')
                result_body += f"""
                <p>Total length: {length}</p>
                <p>A: {a} ({round(a / length * 100, 1)}%)</p>
                <p>C: {c} ({round(c / length * 100, 1)}%)</p>
                <p>G: {g} ({round(g / length * 100, 1)}%)</p>
                <p>T: {t} ({round(t / length * 100, 1)}%)</p>
                """
            elif op == "comp":
                complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
                res_seq = "".join([complement.get(base, 'N') for base in sequence])
                result_body += f"<p>{res_seq}</p>"
            elif op == "rev":
                res_seq = sequence[::-1]
                result_body += f"<p>{res_seq}</p>"

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = f"""
            <html>
                <head><title>Operation Result</title></head>
                <body>
                    {result_body}
                    <br>
                    <a href="/">Main page</a>
                </body>
            </html>
            """
            self.wfile.write(html.encode())

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Not Found</h1>")


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), MyHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()