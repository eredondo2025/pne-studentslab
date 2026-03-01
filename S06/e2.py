class Seq:
    def __init__(self, strbases):
        self.strbases = strbases

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)

def print_seqs(seq_list):
    # Usamos enumerate para obtener tanto el índice (i) como el objeto (s)
    for i, s in enumerate(seq_list):
        print(f"Sequence {i}: (Length: {s.len()}) {s}")

seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]
print_seqs(seq_list)