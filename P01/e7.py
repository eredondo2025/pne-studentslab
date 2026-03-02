from Seq1 import Seq

print("-----| Practice 1, Exercise 6 |------")

s0 = Seq()
s1 = Seq("ACTGA")
s2 = Seq("INVALID")

print(f"Sequence 0: (Length: {len(s0)}) {s0}")
print(f"Bases: {s0.count()}")
print(f"Rev: {s0.reverse()}")
print(f"Sequence 1: (Length: {len(s1)}) {s1}")
print(f"Bases: {s1.count()}")
print(f"Rev: {s1.reverse()}")
print(f"Sequence 2: (Length: {len(s2)}) {s2}")
print(f"Bases: {s2.count()}")
print(f"Rev: {s2.reverse()}")