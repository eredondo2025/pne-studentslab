import http.client
import json

# 1. Define constants
SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
PARAMS = '?content-type=application/json'
URL = SERVER + ENDPOINT + PARAMS

print()
print(f"Server: {SERVER}")
print(f"URL: {URL}")

# 2. Connect with the server
# We use HTTPSConnection because the API uses a secure protocol
conn = http.client.HTTPSConnection(SERVER)

try:
    # Send a GET request to the endpoint with the specified parameters
    conn.request("GET", ENDPOINT + PARAMS)

    # Get the response from the server
    res = conn.getresponse()
    print(f"Response received!: {res.status} {res.reason}")

    # Read the data and decode it from bytes to a UTF-8 string
    data = res.read().decode("utf-8")

    # Parse the JSON string into a Python dictionary
    response = json.loads(data)

    # 3. Check if the server is alive
    # According to Ensembl documentation, a successful ping returns {'ping': 1}
    if response.get('ping') == 1:
        print("\nPING OK! The database is running!")
    else:
        print("\nPING Failed! Unexpected response content.")

except Exception as e:
    print(f"Error connecting to the server: {e}")

    # Always close the connection to free up resources
conn.close()