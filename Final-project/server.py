import os
import json
import http.server
import socketserver
import urllib.request
from urllib.parse import urlparse, parse_qs

PORT = 8080


class EnsemblBioRequestHandler(http.server.BaseHTTPRequestHandler):

    def read_html(self, file_name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "html", file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return f"<h1>Error: File '{file_name}' NOT FOUND </h1>"

    def fetch_ensembl_data(self, url):
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as response:
                data = response.read().decode("utf-8")
                return json.loads(data)
        except Exception as e:
            print(f"Console Log - Connection error with URL ({url}): {e}")
            return None

    def send_html_response(self, html_content, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_json_response(self, data_dict, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        json_string = json.dumps(data_dict, indent=4)
        self.wfile.write(json_string.encode("utf-8"))

    def render_error(self, status_code=404):
        template = self.read_html("error.html")
        self.send_html_response(template, status_code)

    def get_stable_id_by_gene_symbol(self, gene_symbol):
        sanitized_gene = urllib.parse.quote(gene_symbol.strip())
        url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{sanitized_gene}"
        data = self.fetch_ensembl_data(url)
        if data and "id" in data:
            return data["id"]
        return None

    def resolve_species_name(self, user_input):
        url = "https://rest.ensembl.org/info/species"
        data = self.fetch_ensembl_data(url)

        if not data or "species" not in data:
            return None

        user_input = user_input.lower().strip().replace("+", " ")

        for sp in data["species"]:
            display_name = sp.get("display_name", "").lower()
            internal_name = sp.get("name", "").lower()

            if user_input == display_name or user_input == internal_name:
                return sp["name"]

        return None

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        print(f"Console Log - Request path: '{path}'")

        if path == "/" or path == "" or path == "/index.html":
            self.handle_main_endpoint()
        elif path == "/listSpecies":
            self.handle_list_species(query_params)
        elif path == "/karyotype":
            self.handle_karyotype(query_params)
        elif path == "/chromosomeLength":
            self.handle_chromosome_length(query_params)
        elif path == "/geneLookup":
            self.handle_gene_lookup(query_params)
        elif path == "/geneSeq":
            self.handle_gene_seq(query_params)
        elif path == "/geneInfo":
            self.handle_gene_info(query_params)
        elif path == "/geneCalc":
            self.handle_gene_calc(query_params)
        elif path == "/geneList":
            self.handle_gene_list(query_params)
        else:
            self.render_error(404)

    def handle_main_endpoint(self):
        html_content = self.read_html("main.html")
        self.send_html_response(html_content)

    def handle_list_species(self, params):
        limit_val = params.get("limit", [""])[0]
        target_url = "https://rest.ensembl.org/info/species"
        data = self.fetch_ensembl_data(target_url)

        if not data or "species" not in data:
            self.render_error(500)
            return

        species_entries = data["species"]
        if limit_val.isdigit():
            limit = int(limit_val)
            species_entries = species_entries[:limit]
            limit_info = f"{limit} records"
        else:
            limit_info = "all records"

        list_items_html = ""
        for entry in species_entries:
            display_name = entry.get("display_name", "Unknown")
            list_items_html += f"<li>{display_name}</li>\n"

        template = self.read_html("species.html")
        html_output = template.replace("{limit_info}", limit_info).replace("{species_list}", list_items_html)
        self.send_html_response(html_output)

    def handle_karyotype(self, params):
        """
        Endpoint 2: /karyotype - Fully integrated with your helper method
        """
        species = params.get("species", params.get("specie", [""]))[0].strip()
        if not species:
            self.render_error(400)
            return

        # Using your actual resolver method to find the correct scientific name
        resolved_species = self.resolve_species_name(species)
        if not resolved_species:
            resolved_species = species.lower().replace(" ", "_").replace("+", "_")

        safe_species = urllib.parse.quote(resolved_species)
        target_url = f"https://rest.ensembl.org/info/assembly/{safe_species}"
        ensembl_data = self.fetch_ensembl_data(target_url)

        if not ensembl_data:
            self.render_error(404)
            return

        list_badges_html = ""
        if 'karyotype' in ensembl_data:
            for chromo in ensembl_data['karyotype']:
                list_badges_html += f"<li>Chromosome {chromo}</li>\n"
        elif 'top_level_region' in ensembl_data:
            for region in ensembl_data['top_level_region']:
                if region.get("coordinate_system") == "chromosome":
                    chromo_name = region.get("name", "Unknown")
                    list_badges_html += f"<li>Chromosome {chromo_name}</li>\n"

        if not list_badges_html:
            self.render_error(404)
            return

        template = self.read_html("karyotype.html")
        html_output = template.replace("{species_name}", species).replace("{chromosome_badges}", list_badges_html)
        self.send_html_response(html_output)

    def handle_chromosome_length(self, params):
        """
        Endpoint 3: /chromosomeLength - Blinded version without external HTML file dependencies
        """
        # 1. Extract parameters safely
        species = params.get("species", params.get("specie", [""]))[0].strip()
        chromo_target = params.get("chromo", [""])[0].strip()

        if not species or not chromo_target:
            self.render_error(400)
            return

        # 2. Translate the species name using your working internal resolver
        resolved_species = self.resolve_species_name(species)
        if not resolved_species:
            resolved_species = species.lower().replace(" ", "_").replace("+", "_")

        # 3. Fetch data from the university server path
        safe_species = urllib.parse.quote(resolved_species)
        target_url = f"https://rest.ensembl.org/info/assembly/{safe_species}"
        ensembl_data = self.fetch_ensembl_data(target_url)

        if not ensembl_data or 'top_level_region' not in ensembl_data:
            self.render_error(404)
            return

        # 4. Loop through regions and extract the length
        length = None
        for region in ensembl_data['top_level_region']:
            server_chrom_name = str(region.get('name', '')).lower().strip()
            if server_chrom_name == chromo_target.lower().strip():
                length = str(region.get('length'))
                break

        if not length:
            self.render_error(404)
            return

        # 5. HARDCODED HTML RESPONSE: This bypasses read_html() completely to prevent "File NOT FOUND" errors!
        html_output = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chromosome Length</title>
        </head>
        <body>
            <div class="card">
                <h2>Chromosome Data Found Successfully</h2>
                <ul>
                    <li><strong>Species:</strong> {species}</li>
                    <li><strong>Chromosome:</strong> {chromo_target}</li>
                    <li><strong>Length:</strong> {length} base pairs</li>
                </ul>
                <p><a href="/" style="color: #7f8c8d; text-decoration: none;">&larr; Back to Main page</a></p>
            </div>
        </body>
        </html>
        """

        # 6. Deliver the fully rendered webpage directly to your browser
        self.send_html_response(html_output)

    def handle_gene_lookup(self, params):
        gene_symbol = params.get("gene", [""])[0].strip()
        is_json_requested = params.get("json", [""])[0] == "1"

        if not gene_symbol:
            self.render_error(400)
            return

        stable_id = self.get_stable_id_by_gene_symbol(gene_symbol)
        if not stable_id:
            self.render_error(404)
            return

        if is_json_requested:
            json_payload = {"gene": gene_symbol, "id": stable_id}
            self.send_json_response(json_payload)
        else:
            response_html = f"""
            <html>
            <body style="font-family: Arial; margin: 30px;">
                <h2>Gene Lookup Result</h2>
                <p>The stable identifier for gene <strong>{gene_symbol}</strong> is: <code>{stable_id}</code></p>
                <p><a href="/">Back to Dashboard</a></p>
            </body>
            </html>
            """
            self.send_html_response(response_html)

    def handle_gene_seq(self, params):
        gene_symbol = params.get("gene", [""])[0].strip()
        is_json_requested = params.get("json", [""])[0] == "1"

        if not gene_symbol:
            self.render_error(400)
            return

        stable_id = self.get_stable_id_by_gene_symbol(gene_symbol)
        if not stable_id:
            self.render_error(404)
            return

        seq_url = f"https://rest.ensembl.org/sequence/id/{stable_id}?content-type=application/json"
        seq_data = self.fetch_ensembl_data(seq_url)

        if not seq_data or "seq" not in seq_data:
            self.render_error(404)
            return

        gene_sequence = seq_data["seq"]

        if is_json_requested:
            json_payload = {"gene": gene_symbol, "id": stable_id, "sequence": gene_sequence}
            self.send_json_response(json_payload)
        else:
            response_html = f"""
            <html>
            <body style="font-family: Arial; margin: 30px;">
                <h2>Gene Sequence for {gene_symbol} ({stable_id})</h2>
                <textarea rows="15" cols="80" readonly style="font-family: monospace;">{gene_sequence}</textarea>
                <p><a href="/">Back to Dashboard</a></p>
            </body>
            </html>
            """
            self.send_html_response(response_html)

    def handle_gene_info(self, params):
        gene_symbol = params.get("gene", [""])[0].strip()
        is_json_requested = params.get("json", [""])[0] == "1"

        if not gene_symbol:
            self.render_error(400)
            return

        stable_id = self.get_stable_id_by_gene_symbol(gene_symbol)
        if not stable_id:
            self.render_error(404)
            return

        url = f"https://rest.ensembl.org/lookup/id/{stable_id}"
        data = self.fetch_ensembl_data(url)

        if not data:
            self.render_error(404)
            return

        start_pos = data.get("start", "Unknown")
        end_pos = data.get("end", "Unknown")
        chrom_name = data.get("seq_region_name", "Unknown")

        try:
            gene_length = int(end_pos) - int(start_pos) + 1
        except Exception:
            gene_length = "Unknown"

        if is_json_requested:
            json_payload = {
                "gene": gene_symbol,
                "id": stable_id,
                "chromosome": chrom_name,
                "start": start_pos,
                "end": end_pos,
                "length": gene_length
            }
            self.send_json_response(json_payload)
        else:
            response_html = f"""
            <html>
            <body style="font-family: Arial; margin: 30px;">
                <h2>Gene Information: {gene_symbol}</h2>
                <ul>
                    <li><strong>Ensembl ID:</strong> {stable_id}</li>
                    <li><strong>Chromosome Name:</strong> {chrom_name}</li>
                    <li><strong>Start Position:</strong> {start_pos}</li>
                    <li><strong>End Position:</strong> {end_pos}</li>
                    <li><strong>Calculated Length:</strong> {gene_length} base pairs</li>
                </ul>
                <p><a href="/">Back to Dashboard</a></p>
            </body>
            </html>
            """
            self.send_html_response(response_html)

    def handle_gene_calc(self, params):
        gene_symbol = params.get("gene", [""])[0].strip()
        self.send_html_response(f"<h1>Service 7 Calculation - Target Gene: {gene_symbol}</h1>")

    def handle_gene_list(self, params):
        chromo = params.get("chromo", [""])[0].strip()
        start = params.get("start", [""])[0].strip()
        end = params.get("end", [""])[0].strip()
        self.send_html_response(f"<h1>Service 8 Overlap List - Region {chromo}:{start}-{end}</h1>")


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), EnsemblBioRequestHandler) as httpd:
        print(f"==================================================")
        print(f" ADVANCED Server active at http://localhost:{PORT}/")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer offline.")