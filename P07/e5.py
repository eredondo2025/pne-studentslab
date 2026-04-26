import http.client
import json

# 1. Dictionary of genes from Exercise 2
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

SERVER = 'rest.ensembl.org'
PARAMS = '?content-type=application/json'

# 2. Iterate through all genes in the dictionary
for gene_name, gene_id in genes.items():
    ENDPOINT = f'/sequence/id/{gene_id}'
    URL = SERVER + ENDPOINT + PARAMS

    print(f"\nServer: {SERVER}")
    print(f"URL: {URL}")

    # 3. Connect to the server for each gene
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

            total_len = len(sequence)
            print(f"Total lengh: {total_len}")

            # 4. Calculate base statistics
            bases = ['A', 'C', 'G', 'T']
            base_counts = {}

            for b in bases:
                count = sequence.count(b)
                percentage = (count / total_len) * 100
                base_counts[b] = count
                print(f"{b}: {count} ({percentage:.1f}%)")

            # Determine the most frequent base
            most_frequent = max(base_counts, key=base_counts.get)
            print(f"Most frequent Base: {most_frequent}")
            print("-" * 30)  # Separator for readability

        else:
            print(f"ERROR! Could not retrieve data for {gene_name}")

    except Exception as e:
        print(f"Connection Error: {e}")

        conn.close()