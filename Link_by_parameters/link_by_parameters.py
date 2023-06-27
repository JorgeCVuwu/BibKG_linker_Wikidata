#author
import json
import re
import time
import os
import csv

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg linked by id.json"
bibkg_names_path = json_folder + "bibkg_person_name.json"

carpeta_externa = "D:\Memoria" 
wikidata_person_name = "wikidata_person.json"
wikidata_scholar_name = "wikidata_scholar.json"

publications_dict = {}

print("Creando diccionario de publicaciones")

with open(bibkg_names_path, 'r') as bibkg:
    print("Almacenando autores de BibKG")
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'has_author' in entity:
            publications_dict[id] = entity['has_author']

with open():
    print("Comparando con entidades de Wikidata")