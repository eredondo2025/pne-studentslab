import Seq0
FOLDER = "../sequences/"

bases = ["A", "C", "T", "G"]
gene_list = ["U5", "ADA", "FRAT1", "FXN"]
print("-----| Exercise 4 |------")

for gene in gene_list:
    filename = gene + ".txt"
    full_path = FOLDER + filename
    sequence = Seq0.seq_read_fasta(full_path)

    print(f"\nGene {gene}:")
    for b in bases:
        count = Seq0.seq_count_base(sequence, b)
        print(f"  {b}: {count}")