import http.client
import json

# 1. Dictionary from Exercise 2
genes = {
    'FRAT1': 'ENSG00000165879',
    'ADA': 'ENSG00000196839',
    'FXN': 'ENSG00000165060',
    'RNU6-269P': 'ENSG00000212379',
    'MIR633': 'ENSG00000207552',
    'TTTY4C': 'ENSG00000228296',
    'RBMY2YP': 'ENSG00000227633',
    'FGFR3': 'ENSG00000068078',
    'KDR': 'ENSG00000128052',
    'ANK2': 'ENSG00000145362'
}

# 2. Get user input
gene_name = input("Write the gene name: ").strip().upper()

if gene_name in genes:
    gene_id = genes[gene_name]
    SERVER = 'rest.ensembl.org'
    ENDPOINT = f'/sequence/id/{gene_id}'
    PARAMS = '?content-type=application/json'
    URL = SERVER + ENDPOINT + PARAMS

    print(f"\nServer: {SERVER}")
    print(f"URL: {URL}")

    # 3. Connect and fetch data
    conn = http.client.HTTPSConnection(SERVER)
    try:
        conn.request("GET", ENDPOINT + PARAMS)
        res = conn.getresponse()
        print(f"Response received!: {res.status} {res.reason}")

        if res.status == 200:
            data = res.read().decode("utf-8")
            response = json.loads(data)
            sequence = response.get('seq')
            description = response.get('desc')

            print(f"\nGene: {gene_name}")
            print(f"Description: {description}")
            print("New sequence created!")

            # 4. Calculations
            total_len = len(sequence)
            print(f"Total lengh: {total_len}")  # Kept the typo 'lengh' from your screenshot!

            bases = ['A', 'C', 'G', 'T']
            base_counts = {}

            for base in bases:
                count = sequence.count(base)
                percentage = (count / total_len) * 100
                base_counts[base] = count
                print(f"{base}: {count} ({percentage:.1f}%)")

            # Find the most frequent base
            most_frequent = max(base_counts, key=base_counts.get)
            print(f"Most frequent Base: {most_frequent}")

    except Exception as e:
        print(f"Error: {e}")

    conn.close()
else:
    print(f"Error: Gene '{gene_name}' not found in the dictionary.")