from boto3 import client

from Client0 import Client
IP = "212.128.255.91"
PORT = 8080

# Loop to connect 5 times
for i in range(5):
    # Create the message: "Message 0", "Message 1", etc.
    msg = f"Message {i}"

    print(f"To Server: {msg}")
    client = Client(IP, PORT)
    # Send the message and wait for the server's response
    # The talk() method
    response = client.talk(msg)

    print(f"From Server: {response}")