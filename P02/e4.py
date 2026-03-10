from Seq1 import Seq
from Client0 import Client

PRACTICE = 2
EXERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "212.128.255.90" # your IP address
PORT = 8080

# -- Create a client object
c = Client(IP, PORT)

s = Seq()
FOLDER = "../sequences/"
gene_list = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]
for gene in gene_list:
    s.read_fasta(FOLDER + gene)
    print(f"Sending the {gene} Gene to the server...")
    response = c.talk(str(s))
    print(f"To server: {str(s)}")
    print(f"From server: {response}")