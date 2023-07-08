import json
import os

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg.json"
carpeta_externa = "D:\Memoria" 
wikidata_scholar_name = "wikidata_scholar_4.json"
wikidata_person_name = "wikidata_person.json"
wikidata_else_name = "wikidata_else.json"

wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)
wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
wikidata_else_path = os.path.join(carpeta_externa, wikidata_else_name)

count_doi = 0
count_not_doi = 0

with open(wikidata_scholar_path, 'r') as wikidata_person:
    c = 0
    for linea in wikidata_person:
        entity = json.loads(linea)
        id = entity['id']
        claims = entity['claims']
        if 'P50' in claims:
            for author in claims['P50']:
                if 'order' in author:
                    print(id)
                    print(claims['P50'])
                    c+= 1
                    break
                    
            if c > 2:
                break
print(count_doi)
print(count_not_doi)