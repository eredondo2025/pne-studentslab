import Seq0

FOLDER = "../sequences/"
FILENAME = "U5.txt"

full_path = FOLDER + FILENAME
sequence = Seq0.seq_read_fasta(full_path)

print("DNA file: ", FILENAME)
print("The first 20 bases are:")
print(sequence[:20])