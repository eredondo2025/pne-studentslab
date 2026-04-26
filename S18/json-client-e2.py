import http.client
import json

# Connection details
SERVER = "localhost"
PORT = 8080

# 1. Connect to the server
conn = http.client.HTTPConnection(SERVER, PORT)

try:
    # 2. Request the resource /listusers
    conn.request("GET", "/listusers")

    # 3. Get the response
    response = conn.getresponse()
    print(f"Status: {response.status} {response.reason}")

    # 4. Read and parse the JSON data
    data = response.read().decode("utf-8")
    people = json.loads(data)

    # 5. Print the users (Simple print)
    print("\nList of users received from server:")
    for person in people:
        print(f"- {person['Firstname']} {person['Lastname']} (Age: {person['age']})")

except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()