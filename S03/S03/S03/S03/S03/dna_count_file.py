def count_dna(sequences):

    for seq in sequences:
        print("The total lenght: ", len(seq))
        bases = {"A": 0, "C": 0, "G": 0, "T": 0}
        for base in seq:
            if base in bases:
                bases[base] += 1

        for base, count in bases.items():
            print(f'{base}: {count}')

sequences = ["AGTACACTGGT",
"ACCAGTGTACT",
"ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"]

count_dna(sequences)