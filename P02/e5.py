from Seq1 import Seq
from Client0 import Client

PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "212.128.255.71" # your IP address
PORT = 8080

# -- Create a client object
c = Client(IP, PORT)

s = Seq()
FOLDER = "../sequences/"
gene = "FRAT1.txt"
s.read_fasta(FOLDER + gene)
base = s.strbases

for i in range(5):
    start = i * 10
    end = start + 10
    fragment = base[start:end]
    message = f"Fragment {i + 1}: {fragment}"
    response = c.talk(message)
    print(message)

s.read_fasta(FOLDER + "FRAT1.txt")

print(f"Sending the FRAT1.txt Gene to the server...")
response = c.talk(str(s))
print(f"To server: {str(s)}")
print(f"From server: {response}")