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
    def count_base(self):
        if not self.valid or self.strbases == "":
            return "A: 0,   C: 0,   T: 0,   G: 0"
        a = self.strbases.count("A")
        c = self.strbases.count("C")
        t = self.strbases.count("T")
        g = self.strbases.count("G")
        return f"A: {a},   C: {c},   T: {t},   G: {g}"