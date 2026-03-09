from Seq1 import Seq
from Client0 import Client

PRACTICE = 2
EXERCISE = 6

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "212.128.255.90"
# We create both clients
c1 = Client(IP, 8080)
c2 = Client(IP, 8081)

s = Seq()
s.read_fasta("../sequences/FRAT1.txt")

for i in range(10):
    start = i * 10
    end = start + 10
    fragment = s[start:end]
    n_fragment = i + 1
    message = f"Fragment {n_fragment}: {fragment}"

    if n_fragment % 2 != 0:
        response = c1.talk(message)
    else:
        response = c2.talk(message)

    print(message)