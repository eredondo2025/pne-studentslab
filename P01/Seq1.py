class Seq:
    def __init__(self, strbases=None):
        self.valid = True
        self.strbases = strbases if strbases is not None else ""

        if strbases is None:
            print("NULL sequence Created")
            return

        for base in strbases:
            if base not in "ACGT":
                print("INVALID sequence!")
                self.valid = False
                break

        if self.valid:
            print("New sequence created!")

    def __len__(self):
        if self.strbases == "" or not self.valid:
            return 0
        return len(self.strbases)

    def __str__(self):
        if self.strbases == "":
            return "NULL"
        if not self.valid:
            return "ERROR"
        return self.strbases

    def count_base(self, sequence=None):
        if sequence is None:
            sequence = self.strbases

        return {base: sequence.count(base) for base in 'ATCG'}

    def count(self):
        bases = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

        if not self.valid or self.strbases == "":
            return bases
        for base in bases:
            bases[base] = self.strbases.count(base)
        return bases

    def reverse(self):
        if self.strbases == "":
            return "NULL"
        elif not self.valid:
            return "ERROR"
        return self.strbases[::-1]

    def complement(self):
        if self.strbases == "":
            return "NULL"
        elif not self.valid:
            return "ERROR"
        mapping = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return "".join(mapping[base] for base in self.strbases)

    def read_fasta(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line.startswith(">"):
                    self.strbases += line

        self.valid = all(base in 'ATCG' for base in self.strbases)
        self.bases = self.count_base(self.strbases)

