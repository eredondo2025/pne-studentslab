import Seq0
FOLDER = "../sequences/"

gene_list = ["U5", "ADA", "FRAT1", "FXN"]

print("-----| Exercise 3 |------")

for gene in gene_list:
    filename = gene + ".txt"
    full_path = FOLDER + filename
    sequence = Seq0.seq_read_fasta(full_path)
    length = Seq0.seq_len(sequence)

    print("Genes:", gene, "-> Length:", length)