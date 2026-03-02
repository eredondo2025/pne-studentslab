from Seq1 import Seq
FOLDER = "../sequences/"
FILENAME = "U5.txt"
full_path = FOLDER + FILENAME
print("-----| Practice 1, Exercise 9 |------")
s = Seq()
s.read_fasta(full_path)

print(f"Sequence : (Length: {len(s)}) {s.strbases[:20]}...")
print(f"Bases: {s.bases}")
print(f"Rev: {s.reverse()[:20]}...")
print(f"Comp: {s.complement()[:20]}...")