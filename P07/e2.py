# Dictionary with gene names as keys and Ensembl IDs as values
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

print("Dictionary of Genes!")
# Use len() to count the entries in the dictionary
print(f"There are {len(genes)} genes in the dictionary:")
print()

#Iterate through the dictionary to print each entry
# The .items() method allows us to access both the key and the value
for name, identifier in genes.items():
    print(f"{name}: --> {identifier}")