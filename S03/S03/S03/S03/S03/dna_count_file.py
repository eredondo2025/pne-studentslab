#Option 1
#f = open("dna.txt", "r")
#lines = f.read.lines()
#f.close()
#Option 2
with open("dna.txt", "r") as f:
    lines = f.readlines()

total_number = 0
bases = {"A": 0, "C": 0, "G": 0, "T": 0}
for seq in sequences:
    sequence.strip()   #Remove spaces
    total_number += len(sequence)

    for base in seq:
        if base in bases:
            bases[base] += 1

        print("The total number of bases: ", total_number)

        for base, count in bases.items():
            print(f'{base}: {count}')
