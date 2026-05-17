import os
import json
import http.server
import socketserver
import urllib.request
from urllib.parse import urlparse, parse_qs

PORT = 8080


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

    def render_error(self, status_code=404):
        """
        Displays the custom basic red error template.
        """
        template = self.read_html("error.html")
        self.send_html_response(template, status_code)

    def do_GET(self):
        """
        Main HTTP GET Routing Manager.
        """
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == "/":
            self.handle_main_endpoint()
        elif path == "/listSpecies":
            self.handle_list_species(query_params)
        elif path == "/karyotype":
            self.handle_karyotype(query_params)
        elif path == "/chromosomeLength":
            self.handle_chromosome_length(query_params)
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
        Endpoint: /listSpecies - Lists available species from Ensembl.
        """
        limit_val = params.get("limit", [""])[0]

        # Target official Ensembl endpoint with secure HTTPS protocol
        target_url = "https://rest.ensembl.org/info/species"
        data = self.fetch_ensembl_data(target_url)

        if not data or "species" not in data:
            self.render_error(500)
            return

        species_entries = data["species"]

        # Check if the user defined a numerical limit parameter
        if limit_val.isdigit():
            limit = int(limit_val)
            species_entries = species_entries[:limit]
            limit_info = f"{limit} records"
        else:
            limit_info = "all records"

        # Construct individual HTML list item nodes
        list_items_html = ""
        for entry in species_entries:
            display_name = entry.get("display_name", "Unknown")
            list_items_html += f"<li>{display_name}</li>\n"

        template = self.read_html("species.html")
        html_output = template.replace("{limit_info}", limit_info).replace("{species_list}", list_items_html)
        self.send_html_response(html_output)

    def handle_karyotype(self, params):
        """
        Endpoint: /karyotype - Resolves chromosomal structures for a given species.
        """
        # Supports both parameter keys to handle potential form variations safely
        species = params.get("species", params.get("specie", [""]))[0].strip()

        if not species:
            self.render_error(400)
            return

        sanitized_species = urllib.parse.quote(species)
        target_url = f"https://rest.ensembl.org/info/assembly_info/{sanitized_species}"
        data = self.fetch_ensembl_data(target_url)

        if not data or "top_level_region" not in data:
            self.render_error(400)
            return

        # Separate and append only structural genomic chromosomal lines
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
        html_output = template.replace("{species_name}", species).replace("{chromosome_badges}", list_badges_html)
        self.send_html_response(html_output)

    def handle_chromosome_length(self, params):
        """
        Endpoint: /chromosomeLength - Returns total base pair length of a single chromosome.
        """
        species = params.get("species", params.get("specie", [""]))[0].strip()
        chromo = params.get("chromo", [""])[0].strip()

        if not species or not chromo:
            self.render_error(400)
            return

        sanitized_species = urllib.parse.quote(species)
        target_url = f"https://rest.ensembl.org/info/assembly_info/{sanitized_species}"
        data = self.fetch_ensembl_data(target_url)

        if not data or "top_level_region" not in data:
            self.render_error(400)
            return

        # Scan regions to locate the requested chromosome length data
        matched_length = None
        for region in data["top_level_region"]:
            if str(region.get("name")).lower() == chromo.lower():
                matched_length = region.get("length")
                break

        if matched_length is None:
            self.render_error(404)
            return

        template = self.read_html("length.html")
        html_output = template.replace("{species_name}", species) \
            .replace("{chromosome_id}", chromo) \
            .replace("{chromosome_length}", str(matched_length))

        self.send_html_response(html_output)


if __name__ == "__main__":
    # Prevent socket block errors during local server deployments
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), EnsemblBioRequestHandler) as httpd:
        print(f"==================================================")
        print(f" Server active at http://localhost:{PORT}/")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer offline.")