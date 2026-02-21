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
