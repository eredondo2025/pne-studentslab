import os
import json
import http.server
import socketserver
import urllib.request
from urllib.parse import urlparse, parse_qs

PORT = 8081


class EnsemblBioRequestHandler(http.server.BaseHTTPRequestHandler):

    def read_html(self, file_name):
        """
        Reads an HTML file from the 'html' directory using absolute paths.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "html", file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return f"<h1>Error: File '{file_name}' missing inside 'html/' folder.</h1>"

    def fetch_ensembl_data(self, url):
        """
        Connects to the Ensembl REST API using HTTPS and returns parsed JSON data.
        """
        req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            print(f"Console Log - Connection error with URL ({url}): {e}")
            return None

    def send_html_response(self, html_content, status_code=200):
        """
        Sends standard HTTP response headers and HTML payload.
        """
        self.send_response(status_code)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_json_response(self, data_dict, status_code=200):
        """
        ADVANCED LEVEL: Sends pure structured JSON payloads to software clients.
        """
        self.send_response(status_code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        # Convert dictionary to raw text string formatted as JSON
        json_string = json.dumps(data_dict, indent=4)
        self.wfile.write(json_string.encode("utf-8"))

    def render_error(self, status_code=404):
        """
        Displays the custom basic red error template.
        """
        template = self.read_html("error.html")
        self.send_html_response(template, status_code)

    def clean_species_name(self, raw_name):
        """
        Dynamically resolves common names or scientific names into the official
        Ensembl registry name by querying the global species database.
        """
        input_name = raw_name.strip().lower().replace(" ", "_").replace("+", "_")
        if not input_name:
            return ""

        species_url = "https://rest.ensembl.org/info/species"
        database_json = self.fetch_ensembl_data(species_url)

        if not database_json or "species" not in database_json:
            return input_name

        for entry in database_json["species"]:
            scientific_name = entry.get("name", "")
            common_name = entry.get("common_name", "").lower().replace(" ", "_")
            display_name = entry.get("display_name", "").lower().replace(" ", "_")
            aliases = [alias.lower().replace(" ", "_") for alias in entry.get("aliases", [])]

            if input_name in (scientific_name, common_name, display_name) or input_name in aliases:
                return scientific_name

        return input_name

    def get_stable_id_by_gene_symbol(self, gene_symbol):
        """
        Helper method to resolve a gene symbol (e.g., FRAT1) into an Ensembl stable ID (ENSG...).
        """
        sanitized_gene = urllib.parse.quote(gene_symbol.strip())
        url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{sanitized_gene}"
        data = self.fetch_ensembl_data(url)
        if data and "id" in data:
            return data["id"]
        return None

    def do_GET(self):
        """
        Main HTTP GET Routing Manager. Matches all 8 endpoints from basic and medium levels.
        """
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        print(f"Console Log - Incoming request path: '{path}'")

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
        """
        Serves the visual interactive dashboard (main.html).
        """
        html_content = self.read_html("main.html")
        self.send_html_response(html_content)

    def handle_list_species(self, params):
        """
        Endpoint 1: /listSpecies
        """
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
        Endpoint 2: /karyotype
        """
        raw_species = params.get("species", params.get("specie", [""]))[0]
        species = self.clean_species_name(raw_species)

        if not species:
            self.render_error(400)
            return

        sanitized_species = urllib.parse.quote(species)
        target_url = f"https://rest.ensembl.org/info/assembly_info/{sanitized_species}"
        data = self.fetch_ensembl_data(target_url)

        if not data or "top_level_region" not in data:
            self.render_error(400)
            return

        chromosomes = []
        for region in data["top_level_region"]:
            if region.get("coordinate_system") == "chromosome":
                chromosomes.append(region.get("name", "Unknown"))

        if not chromosomes:
            list_badges_html = "<p>No chromosomes found for this organism.</p>"
        else:
            list_badges_html = ""
            for chromo_name in chromosomes:
                list_badges_html += f"<li>Chromosome {chromo_name}</li>\n"

        template = self.read_html("karyotype.html")
        html_output = template.replace("{species_name}", raw_species).replace("{chromosome_badges}", list_badges_html)
        self.send_html_response(html_output)

    def handle_chromosome_length(self, params):
        """
        Endpoint 3: /chromosomeLength
        """
        raw_species = params.get("species", params.get("specie", [""]))[0]
        chromo = params.get("chromo", [""])[0].strip()
        species = self.clean_species_name(raw_species)

        if not species or not chromo:
            self.render_error(400)
            return

        sanitized_species = urllib.parse.quote(species)
        target_url = f"https://rest.ensembl.org/info/assembly_info/{sanitized_species}"
        data = self.fetch_ensembl_data(target_url)

        if not data or "top_level_region" not in data:
            self.render_error(400)
            return

        matched_length = None
        for region in data["top_level_region"]:
            if str(region.get("name")).lower() == chromo.lower():
                matched_length = region.get("length")
                break

        if matched_length is None:
            self.render_error(404)
            return

        template = self.read_html("length.html")
        html_output = template.replace("{species_name}", raw_species) \
            .replace("{chromosome_id}", chromo) \
            .replace("{chromosome_length}", str(matched_length))
        self.send_html_response(html_output)

    # =========================================================================
    # ADVANCED HYBRID ENDPOINTS (SERVICES 4 TO 6 FULLY IMPLEMENTED)
    # =========================================================================

    def handle_gene_lookup(self, params):
        """
        Endpoint 4: /geneLookup - Fetches stable identifier of a human gene symbol.
        Supports web view or dynamic REST JSON output.
        """
        gene_symbol = params.get("gene", [""])[0].strip()
        is_json_requested = params.get("json", [""])[0] == "1"

        if not gene_symbol:
            self.render_error(400)
            return

        stable_id = self.get_stable_id_by_gene_symbol(gene_symbol)
        if not stable_id:
            self.render_error(404)
            return

        # ADVANCED LEVEL CHECK: If json=1 parameter is present, send data object
        if is_json_requested:
            json_payload = {"gene": gene_symbol, "id": stable_id}
            self.send_json_response(json_payload)
        else:
            # Medium Level standard HTML view response
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
        """
        Endpoint 5: /geneSeq - Returns the raw nucleotide sequence of a human gene.
        Supports web view or dynamic REST JSON output.
        """
        gene_symbol = params.get("gene", [""])[0].strip()
        is_json_requested = params.get("json", [""])[0] == "1"

        if not gene_symbol:
            self.render_error(400)
            return

        stable_id = self.get_stable_id_by_gene_symbol(gene_symbol)
        if not stable_id:
            self.render_error(404)
            return

        seq_url = f"https://rest.ensembl.org/sequence/id/{stable_id}"
        seq_data = self.fetch_ensembl_data(seq_url)

        if not seq_data or "seq" not in seq_data:
            self.render_error(404)
            return

        gene_sequence = seq_data["seq"]

        # ADVANCED LEVEL CHECK
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
        """
        Endpoint 6: /geneInfo - Returns start, end, length, id, and chromosome name.
        Supports web view or dynamic REST JSON output.
        """
        gene_symbol = params.get("gene", [""])[0].strip()
        is_json_requested = params.get("json", [""])[0] == "1"

        if not gene_symbol:
            self.render_error(400)
            return

        sanitized_gene = urllib.parse.quote(gene_symbol)
        url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{sanitized_gene}"
        data = self.fetch_ensembl_data(url)

        if not data or "id" not in data:
            self.render_error(404)
            return

        start_pos = data.get("start", "Unknown")
        end_pos = data.get("end", "Unknown")
        chrom_name = data.get("seq_region_name", "Unknown")
        stable_id = data.get("id", "Unknown")

        try:
            gene_length = int(end_pos) - int(start_pos) + 1
        except Exception:
            gene_length = "Unknown"

        # ADVANCED LEVEL CHECK
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
        """
        Endpoint 7: /geneCalc - Fallback template for non-implemented medium services
        """
        gene_symbol = params.get("gene", [""])[0].strip()
        self.send_html_response(f"<h1>Service 7 Calculation - Target Gene: {gene_symbol}</h1>")

    def handle_gene_list(self, params):
        """
        Endpoint 8: /geneList - Fallback template for non-implemented medium services
        """
        chromo = params.get("chromo", [""])[0].strip()
        start = params.get("start", [""])[0].strip()
        end = params.get("end", [""])[0].strip()
        self.send_html_response(f"<h1>Service 8 Overlap List - Region {chromo}:{start}-{end}</h1>")


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), EnsemblBioRequestHandler) as httpd:
        print(f"==================================================")
        print(f" ADVANCED Server active at http://localhost:{PORT}/")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer offline.")