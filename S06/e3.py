from Seq0 import Seq
def generate_seqs(pattern, number):
    seq_list = []
    for i in range(1, number + 1):
        seq_str = pattern * i
        new_seq = Seq(seq_str)
        seq_list.append(new_seq)

    return seq_list

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print("List 1:")
print_seqs(seq_list1)

print()
print("List 2:")
print_seqs(seq_list2)