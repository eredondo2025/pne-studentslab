dna = "ATGCGATCGATCGATCGATCGA"

print("Length: ", len(dna))
print("First 5 : ", dna[0:5])
print("Last 5: ", dna[-3:])
print(dna.lower())
print("ATC count: ", dna.count("ATC"))
print("RNA: ", dna.replace("T", "U"))