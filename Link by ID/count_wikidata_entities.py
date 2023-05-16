import json
import os

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg.json"
carpeta_externa = "D:\Memoria" 
wikidata_scholar_name = "wikidata_scholar.json"
wikidata_else_name = "wikidata_else.json"

wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)
wikidata_else_path = os.path.join(carpeta_externa, wikidata_else_name)


with open(wikidata_scholar_path, 'r') as wikidata_scholar:
    for linea in wikidata_scholar:
        entity = json.loads(linea)
        id = entity['id']
        claims = entity['claims']
        linked = False
        if id == "Q26883131":
            print(entity)
            break