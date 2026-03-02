class Seq:
    def __init__(self, strbases=None):
        if strbases is None:
            print("NULL sequence Created")
            self.strbases = ""
            return
        self.valid = True
        for base in strbases:
            if base not in "ACGT":
                print("INVALID sequence!")
                self.valid = False
                break
        if self.valid:
            print("New sequence created!")
        self.strbases = strbases

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