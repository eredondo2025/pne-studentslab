import Seq0

FOLDER = "../sequences/"
FILENAME = "U5.txt"
print("-----| Exercise 7 |------")
full_path = FOLDER + FILENAME
sequence = Seq0.seq_read_fasta(full_path)
n_base = 20
fragment = sequence[:n_base]
complement = Seq0.seq_complement(fragment)

print(f"Gene {FILENAME}:")
print(f"Frag: {fragment}")
print(f"Comp: {complement}")