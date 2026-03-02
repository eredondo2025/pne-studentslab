from Seq1 import Seq
print("-----| Practice 1, Exercise 5 |------")

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")
print(f"Sequence 1: (Length: {len(s1)}) {s1}  {s1.count_base()}")
print(f"Sequence 2: (Length: {len(s2)}) {s2} {s2.count_base()}")
print(f"Sequence 3: (Length: {len(s3)}){s3} {s3.count_base()}")