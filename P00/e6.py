import Seq0

FOLDER = "../sequences/"
FILENAME = "U5.txt"
print("-----| Exercise 6 |------")
full_path = FOLDER + FILENAME
sequence = Seq0.seq_read_fasta(full_path)

n_base = 20
fragment = sequence[:n_base]
reverse_fragment = Seq0.seq_reverse(sequence, n_base)

print(f"Gene {FILENAME}")
print(f"Fragment: {fragment}")
print(f"Reverse:  {reverse_fragment}")