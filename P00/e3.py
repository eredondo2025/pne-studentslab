import Seq0
FOLDER = "../sequences/"

gene_list = ["ADA", "FRAT1", "FXN", "U5"]

print("-----| Exercise 3 |------")

for gene in gene_list:
    filename = gene + ".txt"
    full_path = FOLDER + filename
    sequence = Seq0.seq_read_fasta(full_path)
    length = Seq0.seq_len(sequence)

    print("Gene: ", gene, "-> Length: ", length)