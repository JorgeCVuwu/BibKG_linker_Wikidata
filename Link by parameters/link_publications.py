import json
import re
import time
import os
import csv
import traceback

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg linked authors.json"
bibkg_names_path = json_folder + "bibkg_person_name.json"
bibkg_linked_path = json_folder + "bibkg linked publications.json"

carpeta_externa = "D:\Memoria" 
wikidata_person_name = "wikidata_person_3.json"
wikidata_scholar_name = "wikidata_scholar_3.json"

wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

bibkg_publications_dict = {}
wikidata_person_dict = {}

wikidata_author_property = 'P50'

links_dict = {}
link_counts_dict = {}
count_links = 0

def is_number(string):
    patron = r'^\d+$'
    if re.match(patron, string):
        return True
    else:
        return False

def process_names(name):
    split = name.split()
    resultado = name
    if len(split) == 3:
        if (len(split[1]) == 2 and "." in split[1]) or len(split[1]) == 1:
            resultado = split[0] + ' ' + split[2]
        elif is_number(split[2]):
            resultado = split[0] + ' ' + split[1]
        # else:
        #     print(name)
    return resultado.replace(".", "")

def process_author_id(id):
    if id[0:2] == "a_":
        return id[2:].replace("_", " ")
    

def link_author(links_dict, bibkg_id, id, link_counts_dict = link_counts_dict):
    if bibkg_id not in links_dict:
        links_dict[bibkg_id] = id

    if bibkg_id not in link_counts_dict:
        link_counts_dict[bibkg_id] = {}
    if id not in link_counts_dict[bibkg_id]:
        link_counts_dict[bibkg_id][id] = 0
    link_counts_dict[bibkg_id][id] += 1

inicio = time.time()

print("Almacenando autores de BibKG")

author_name_dict = {}
author_wikidata_id_dict = {}
with open(bibkg_path, 'r') as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'type' in entity:
            entity_type = entity['type']
            if entity_type == 'Person' and 'wikidata' in entity:
                author_name_dict[id] = {'id':id, 'name':entity['name'], 'publications':{}}
                author_wikidata_id_dict[entity['wikidata']] = author_name_dict[id]
                

print("Almacenando publicaciones de BibKG en autores")

with open(bibkg_path, 'r') as bibkg:
    for linea in bibkg:
        break_c = False
        entity = json.loads(linea)
        id = entity['id']
        if 'has_author' in entity:
            for author in entity['has_author']:
                author_value = author['value']
                if author_value in author_name_dict:
                    author_entity = {}
                    if 'name' in entity:
                        try:
                            author_entity['name'] = process_names(str(entity['name']))
                        except:
                            print(entity)
                            print(entity['name'])
                            break_c = True
                            break
                    author_name_dict[author_value]['publications'][id] = author_entity
            if break_c:
                break

print("Almacenando autores de Wikidata")

count_wikidata_authors = 0
count_wikidata_publications = 0
wikidata_author_dict = {}
with open(wikidata_person_path, 'r') as wikidata_person:
    for linea in wikidata_person:
        entity = json.loads(linea)
        id = entity['id']
        if id in author_wikidata_id_dict:
            wikidata_author_dict[id] = {'id':id, 'publications':{}}
            count_wikidata_authors += 1

print(count_wikidata_authors)
print("Almacenando publicaciones de autores de Wikidata")
with open(wikidata_scholar_path, 'r') as wikidata_scholar:
    for linea in wikidata_scholar:
        break_c = False
        entity = json.loads(linea)
        id = entity['id']
        claims = entity['claims']
        if wikidata_author_property in claims:
            authors = claims[wikidata_author_property]
            for author in authors:
                if 'datavalue' in author['mainsnak']:
                    wikidata_author_id = author['mainsnak']['datavalue']['value']
                    if wikidata_author_id in wikidata_author_dict:
                        author_entity = {}
                        if 'name' in entity:
                            try:
                                #author_entity['name'] = process_names(entity['name']['en']['value'])
                                if len(entity['name']) > 0:
                                    author_entity['name'] = process_names(entity['name'][next(iter(entity['name']))]['value'])
                            except:
                                print(entity)
                                print(entity['name'])
                                break_c = True
                                traceback.print_exc()
                                break
                        wikidata_author_dict[wikidata_author_id]['publications'][id] = author_entity
                        count_wikidata_publications += 1
            if break_c:
                break
print(count_wikidata_publications)

print("Comparando publicaciones de autores")
count_links = 0
for key, wikidata_entity in wikidata_author_dict.items():
    wikidata_publications = wikidata_entity['publications']
    bibkg_entity = author_wikidata_id_dict[key]
    bibkg_publications = bibkg_entity['publications']
    name_values = [publication['name'] for publication in bibkg_publications.values()]
    repeated_names = set()
    for name in name_values:
        if name_values.count(name) > 1:
            repeated_names.add(name)
    for bibkg_key, bibkg_publication in bibkg_publications.items():
        bibkg_name = bibkg_publication['name']
        # definir parametros de comparacion
        for wikidata_key, value in wikidata_publications.items():
            if 'name' in value and bibkg_name not in repeated_names and bibkg_name == value['name']:
                links_dict[bibkg_key] = wikidata_key
                count_links += 1

print("Escribiendo enlaces en BibKG")

count_links_writed = 0

with open(bibkg_path, 'r') as bibkg, open(bibkg_linked_path, 'w') as bibkg_linked_publications:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if id in links_dict and 'wikidata' not in entity:
            wikidata_id = links_dict[id]
            entity['wikidata'] = wikidata_id
            count_links_writed += 1
        json.dump(entity, bibkg_linked_publications)
        bibkg_linked_publications.write("\n")

fin = time.time()

print("Tiempo de ejecución: {} segundos".format(fin - inicio))

print("Relaciones totales encontradas: {}".format(count_links))

print("Enlaces totales escritos en BibKG: {}".format(count_links_writed))
        

