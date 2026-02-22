import Seq0
FOLDER = "../sequences/"
gene_list = ["U5", "ADA", "FRAT1", "FXN"]

print("-----| Exercise 8 |------")

for gene in gene_list:
    filename = FOLDER + gene + ".txt"
    sequence = Seq0.seq_read_fasta(filename)

    counts = Seq0.seq_count(sequence)
    most_frequent = max(counts, key = counts.get)

    print(f"Gene {gene}: Most frequent Base: {most_frequent}")