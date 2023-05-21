import json
import os

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg.json"
carpeta_externa = "D:\Memoria" 
wikidata_scholar_name = "wikidata_scholar.json"
wikidata_else_name = "wikidata_else.json"

wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)
wikidata_else_path = os.path.join(carpeta_externa, wikidata_else_name)

count_doi = 0
count_not_doi = 0

with open(wikidata_scholar_path, 'r') as wikidata_scholar:
    for linea in wikidata_scholar:
        entity = json.loads(linea)
        id = entity['id']
        claims = entity['claims']
        linked = False
        if 'P356' in claims:
            count_doi += 1
        else:
            count_not_doi += 1

print(count_doi)
print(count_not_doi)