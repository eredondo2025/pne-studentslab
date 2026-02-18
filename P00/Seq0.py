from Seq0 import *
def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    from pathlib import Path

    file_path = Path(filename)
    content = file_path.read_text()
    lines = content.splitlines()

    body = "".join(lines[1:])

    return body

def seq_len(seq):
    return len(seq)