import csv
import os

header = ['property', 'name', 'count']

PubMedID = ['P698', 'PubMedID', 62947068]
apparent_magnitude = ['P1215', 'apparent magnitude', 33122953]
astronomical_filter = ['P1227', 'astronomical filter', 	33122898]
PMCID = ['P932', 'PMCID', 11694468]
based_on_heuristic = ['P887', 'based on heuristic', 8566543]
SIMBAD_ID = ['P3083', 'SIMBAD ID', 8152400]
right_ascension = ['P6257', 'right ascension', 8094538]
declination = ['P6258', 'declination', 8094414]
constelation = ['P59','constelation', 7374786]
found_in_taxon = ['P703', 'found in taxon', 7168473]
GeoNames_ID = ['P5875', 'GeoNames ID', 3803157]
GBIF_taxon_ID = ['P846', 'GBIF taxon ID', 3243769]
Entrez_Gene_ID = ['P351', 'Entrez Gene ID', 3116063]
GNS_Unique_Feature_ID = ['P2326', 'GNS Unique Feature ID', 2894821] 
UniProt_protein_ID = ['P352', 'UniProt protein ID', 2537311] 




datos = [
    header,
    PubMedID,
    apparent_magnitude,
    astronomical_filter,
    PMCID,
    based_on_heuristic,
    SIMBAD_ID,
    right_ascension,
    declination,
    constelation,
    found_in_taxon,
    GeoNames_ID,
    GBIF_taxon_ID,
    Entrez_Gene_ID,
    GNS_Unique_Feature_ID,
    UniProt_protein_ID
]

path = r"C:\Users\jorge\OneDrive\Escritorio\Memoria\BibKG-linker---Wikidata\Wikidata parser\data\discarded_properties.csv"

# Abra el archivo CSV para escribir
with open(path, mode='w', newline='') as archivo_csv:
    
    # Crea el objeto de escritura de CSV
    writer = csv.writer(archivo_csv)
    
    # Escriba los datos en el archivo CSV
    for fila in datos:
        writer.writerow(fila)

print("Archivo CSV creado exitosamente.")