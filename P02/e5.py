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
base = s.read_fasta(FOLDER + gene)

for i in range(0, 5):
    l = base[10 * i : 10]
    response = c.talk(str(l))

    #TERMINAR POR AQUI

for gene in gene:
    s.read_fasta(FOLDER + gene)
    print(f"Sending the {gene} Gene to the server...")
    response = c.talk(str(s))
    print(f"To server: {str(s)}")
    print(f"From server: {response}")