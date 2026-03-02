class Seq:
    def __init__(self, strbases=None):
        if strbases is None:
            print("NULL sequence Created")
            self.strbases = ""
            return
        print("New sequence created!")
        self.strbases = strbases

    def __len__(self):
        return len(self.strbases)

    def __str__(self):
        if self.strbases == "":
            return "NULL"
        return self.strbases