import json
import os

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg.json"
carpeta_externa = "D:\Memoria" 
wikidata_scholar_name = "wikidata_scholar.json"
wikidata_person_name = "wikidata_person.json"
wikidata_else_name = "wikidata_else.json"

wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)
wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
wikidata_else_path = os.path.join(carpeta_externa, wikidata_else_name)

count_doi = 0
count_not_doi = 0

with open(wikidata_person_path, 'r') as wikidata_person:
    for linea in wikidata_person:
        entity = json.loads(linea)
        id = entity['id']
        claims = entity['claims']
        if 'P50' in claims:
            print(id)
            print(entity['claims']['P50'])
            break
print(count_doi)
print(count_not_doi)