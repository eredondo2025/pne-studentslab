import Seq0

FOLDER = "../sequences/"
gene_list = ["U5", "ADA", "FRAT1", "FXN"]

print("-----| Exercise 5 |------")

for gene in gene_list:
    filename = FOLDER + gene + ".txt"
    sequence = Seq0.seq_read_fasta(filename)

    diccionario_bases = Seq0.seq_count(sequence)

    print(f"Gene {gene}: {diccionario_bases}")