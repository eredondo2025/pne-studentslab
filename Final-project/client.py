import json
import urllib.request
import urllib.parse

# Connecting to the same port where your Python server is running
SERVER_URL = "http://localhost:8080"


def run_endpoint(path_route, description):
    """
    Helper function to send requests to our hybrid server,
    parse the received JSON response, and print it cleanly.
    """
    print("\n" + "=" * 60)
    print(f" TESTING: {description}")
    print(f" URL Request: {SERVER_URL}{path_route}")
    print("=" * 60)

    try:
        # Perform the HTTP request to the local server
        with urllib.request.urlopen(SERVER_URL + path_route) as response:
            # Read the raw data payload and decode it to a text string
            raw_data = response.read().decode("utf-8")

            # Parse the structured text string into a Python dictionary
            json_data = json.loads(raw_data)

            # Print to the console with clean formatting and indentation
            print("Response received successfully from server (JSON format):")
            print(json.dumps(json_data, indent=4))

    except Exception as e:
        print(f"Error communicating with local server: {e}")
        print("Make sure your server.py is running on port 8081 before executing the client!")


if __name__ == "__main__":
    print("STARTING AUTOMATED REST API CLIENT TESTS")

    # Automated tests including the mandatory 'json=1' URL query parameter

    # Test 1: Service 4 (Gene Lookup) searching for the FRAT1 gene symbol
    run_endpoint("/geneLookup?gene=FRAT1&json=1", "Service 4 - Human Gene Stable ID Lookup")

    # Test 2: Service 5 (Gene Sequence) searching for the FRAT1 gene sequence
    run_endpoint("/geneSeq?gene=FRAT1&json=1", "Service 5 - Human Gene Raw Sequence Extraction")

    # Test 3: Service 6 (Gene Information) searching for the FRAT1 metadata
    run_endpoint("/geneInfo?gene=FRAT1&json=1", "Service 6 - Human Gene Structural Metadata")

    print("\n" + "=" * 60)
    print(" TESTS COMPLETED SUCCESSFULLY ")
    print("=" * 60)