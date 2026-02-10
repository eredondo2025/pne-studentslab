sequence = input("Input a DNA sequence")
print("The total lenght: ", len(sequence))

bases = {"A": 0, "C": 0, "G": 0, "T": 0}

for base in sequence:
    if base in bases:
        bases[base] += 1

for base, count in bases.items():
    print(f'{base}: {count}')

