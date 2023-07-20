import json
import os
import time
from urllib.parse import urlparse
import csv
import ujson

bibkg_url = "bibkg.json"

carpeta_externa = "D:\Memoria" 

wikidata_person_file = "wikidata_person_3.json"
wikidata_scholar_file = "wikidata_scholar_3.json"
wikidata_else_file = "wikidata_else_3.json"
wikidata_filtered_person_file = "wikidata_person_filtered.json"

wikidata_person_csv_file = "wikidata_person_counts.csv"

wikidata_person_url = os.path.join(carpeta_externa, wikidata_person_file)
wikidata_scholar_url = os.path.join(carpeta_externa, wikidata_scholar_file)
wikidata_else_url = os.path.join(carpeta_externa, wikidata_else_file)

wikidata_person_csv_url = os.path.join(carpeta_externa, wikidata_person_csv_file)

filename = wikidata_person_url
new_person_filename = os.path.join(carpeta_externa, '')

c = 0
inicio = time.time()


person_dict = {}

with open(wikidata_scholar_url, 'r') as archivo_json:
    for linea in archivo_json:
        diccionario = json.loads(linea)
        claims = diccionario['claims']
        if "P50" in claims:
            authors = claims['P50']
            for author in authors:
                try:
                    author_id = author['mainsnak']['datavalue']['value']
                except:
                    author_id = "unknown"
                if author_id not in person_dict:
                    person_dict[author_id] = 0
                person_dict[author_id] += 1
        
print("Lectura de publicaciones completada")

with open(wikidata_person_url, 'r') as archivo_json, open(wikidata_filtered_person_file, "w") as person_filtered:
    empty_person = True
    for linea in archivo_json:
        diccionario = json.loads(linea)
        id = diccionario['id']
        if id in person_dict:
            if not empty_person:
                person_filtered.write('\n')
            ujson.dump(diccionario, person_filtered)
            empty_person = False



fin = time.time()
print("Tiempo de ejecución: {} segundos".format(fin - inicio))

archivo_json.close()

print("Escribiendo CSV de counts de Wikidata")

with open(wikidata_person_csv_url, mode='w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(["ID", "Count"])
    sorted_items = sorted(person_dict.items(), key=lambda x: x[1], reverse=True)
    for llave, numero in sorted_items:
        writer.writerow([llave, numero])