class Seq:
    def __init__(self, strbases):
        bases = ["A", "C", "G", "T"]

        for i in strbases:
            if i not in bases:
                self.strbases = "ERROR"
                print("ERROR")
                return
        print("New sequence created!")

s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")
