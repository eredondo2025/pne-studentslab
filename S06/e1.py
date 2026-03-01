class Seq:
    def __init__(self, strbases):
        valid_bases = {'A', 'C', 'G', 'T'}
        is_valid = True

        for base in strbases:
            if base not in valid_bases:
                is_valid = False
                break

        if is_valid:
            self.strbases = strbases
            print("New sequence created!")
        else:
            self.strbases = "ERROR"
            print("ERROR !!")

    def __str__(self):
        return self.strbases

s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")