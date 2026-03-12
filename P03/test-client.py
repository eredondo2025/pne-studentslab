from P02.Client0 import Client
import termcolor

IP = "127.0.0.1"
PORT = 8080


def run_test():
    c = Client(IP, PORT)

    print("-----| Practice 3, Exercise 7 |------")
    print(c)

    print("* Testing PING...")
    response = c.talk("PING")
    print(response.strip())

    print("\n* Testing GET...")
    seq0 = ""
    for i in range(5):
        response = c.talk(f"GET {i}").strip()
        print(f"GET {i}: {response}")
        if i == 0:
            seq0 = response

    print("\n* Testing INFO...")
    info_response = c.talk(f"INFO {seq0}")
    print(info_response.strip())

    print("\n* Testing COMP...")
    comp_response = c.talk(f"COMP {seq0}")
    print(f"COMP {seq0}")
    print(comp_response.strip())

    print("\n* Testing REV...")
    rev_response = c.talk(f"REV {seq0}")
    print(f"REV {seq0}")
    print(rev_response.strip())

    print("\n* Testing GENE...")
    genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
    for gene in genes:
        print(f"GENE {gene}")
        gene_response = c.talk(f"GENE {gene}").strip()

        lines = gene_response.split('\n')
        if len(lines) > 2:
            print(lines[0])
            print("[...]")
            print(lines[-1])
        else:
            print(gene_response)
        print()

if __name__ == "__main__":
    run_test()