from Seq0 import *
def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    from pathlib import Path

    file_path = Path(filename)
    content = file_path.read_text()
    lines = content.splitlines()

    body = [line.strip() for line in lines[1:] if line.strip()]
    clean_body = "".join(body)

    return clean_body

def seq_len(seq):
    return len(seq)

def seq_count_base(seq, base):
    count = 0
    for b in seq:
        if b == base:
            count += 1
    return count


def seq_count(seq):
    counts = {'A': 0, 'C': 0, 'T': 0, 'G': 0}
    for base in seq:
        if base in counts:
            counts[base] += 1

    return counts