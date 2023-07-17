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

doi_dict = {}

with open(wikidata_scholar_path, 'r') as wikidata:
    c = 0
    for linea in wikidata:
        entity = json.loads(linea)
        id = entity['id']
        claims = entity['claims']
        if 'P356' in claims:
            for value in claims['P356']:
                if 'datavalue' in value['mainsnak']:
                    doi = value['mainsnak']['datavalue']['value']
                    doi_dict.setdefault(doi, [])
                    doi_dict[doi].append(id) 

count_doi_repetitions = 0
count_entities = 0
for key, value in doi_dict.items():
    if len(value) >= 2:
        count_doi_repetitions += 1
        count_entities += len(value) #- 1

print(count_doi_repetitions)
print(count_entities)