import http.client
import json

# 1. Define constants
SERVER = 'rest.ensembl.org'
# Stable ID for MIR633 obtained in Exercise 2
GENE_ID = 'ENSG00000207552'
ENDPOINT = f'/sequence/id/{GENE_ID}'
PARAMS = '?content-type=application/json'
URL = SERVER + ENDPOINT + PARAMS

print(f"Server: {SERVER}")
print(f"URL: {URL}")

# 2. Connect with the server
conn = http.client.HTTPSConnection(SERVER)

try:
    # Send the GET request to fetch the sequence of the gene
    conn.request("GET", ENDPOINT + PARAMS)

    # Get the response
    res = conn.getresponse()
    print(f"Response received!: {res.status} {res.reason}")

    # Check if the request was successful
    if res.status == 200:
        # Read and parse the JSON data
        data = res.read().decode("utf-8")
        response = json.loads(data)

        # 3. Print the requested information
        print()
        print(f"Gene: MIR633")
        # The API returns 'desc' for the description and 'seq' for the bases
        print(f"Description: {response.get('desc')}")
        print(f"Bases: {response.get('seq')}")
    else:
        print(f"Error: Unable to retrieve data. Status code: {res.status}")

except Exception as e:
    print(f"Error connecting to the server: {e}")

# Close the connection
conn.close()