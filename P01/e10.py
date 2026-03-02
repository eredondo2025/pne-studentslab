from Seq1 import Seq
FOLDER = "../sequences/"
files = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt", "RNU6_269P.txt"]

print("-----| Practice 1, Exercise 10 |------")
for filename in files:
    s = Seq()
    s.read_fasta(FOLDER + filename)
    gene_name = filename.replace(".txt", "")
    print(f"Gene {gene_name}: Most frequent Base: {s.most_frequent_base()}")
