import json
import os
import time
from urllib.parse import urlparse
import csv
import ujson

def process_wikidata_dblp_id(id):
    if id[:10] == "homepages/":
        id_sin_homepages = id[10:]
        return id_sin_homepages
    else:
        return None

bibkg_url = "bibkg.json"

carpeta_externa = "D:\Memoria" 

wikidata_person_file = "wikidata_person_3.json"
wikidata_scholar_file = "wikidata_scholar_3.json"
wikidata_else_file = "wikidata_else_3.json"
wikidata_filtered_person_file = "wikidata_person.json"

wikidata_person_csv_file = "wikidata_person_counts.csv"

wikidata_person_url = os.path.join(carpeta_externa, wikidata_person_file)
wikidata_scholar_url = os.path.join(carpeta_externa, wikidata_scholar_file)
wikidata_else_url = os.path.join(carpeta_externa, wikidata_else_file)
wikidata_filtered_person_url = os.path.join(carpeta_externa, wikidata_filtered_person_file)

wikidata_person_csv_url = os.path.join(carpeta_externa, wikidata_person_csv_file)

filename = wikidata_person_url
new_person_filename = os.path.join(carpeta_externa, '')

c = 0
inicio = time.time()


person_dict = {}

#Person

#Person.key -> P2456 (DBLP Author ID)
property_bibkg_dblp = 'key'
property_dblp = 'P2456'
wikidata_dblp_dict = {}

#Person.orcid -> P496 (ORCID iD)
property_bibkg_orcid = 'orcid'
property_orcid = 'P496'
wikidata_orcid_dict = {}

#Person.scholar -> P1960 (Google Scholar Author ID)
property_bibkg_scholar = 'scholar'
property_scholar = 'P1960'
wikidata_scholar_dict = {}

count_person = 0
count_links = 0
count_links_dblp = 0
count_links_orcid = 0
count_links_scholar = 0
count_not_links = 0

with open(wikidata_person_url, 'r') as wikidata_person:
    for linea in wikidata_person:
        entity = json.loads(linea)
        id = entity['id']
        claims = entity['claims'].items()
        for key, content in claims:
            try:
                content = content[0]['mainsnak']['datavalue']['value']
                if key == property_dblp:
                    wikidata_dblp_dict[content] = id
                if key == property_orcid:
                    wikidata_orcid_dict[content] = id
                if key == property_scholar:
                    wikidata_scholar_dict[content] = id
            except:
                pass

print("Wikidata cargado")

count_url = 0

with open(bibkg_url, 'r') as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        is_person = False
        if 'has_author' in entity:
            count_url += 1
            #print(entity)
        if 'type' in entity:
            if entity['type'] == 'Person':
                count_person += 1
                is_person = True
        if 'wikidata' in entity:
            continue
        elif property_bibkg_dblp in entity:
            if process_wikidata_dblp_id(entity[property_bibkg_dblp]) in wikidata_dblp_dict:
                count_links += 1
                count_links_dblp += 1
        elif property_bibkg_orcid in entity:
            if entity[property_bibkg_orcid] in wikidata_orcid_dict:
                count_links += 1
                count_links_orcid += 1
        
        elif property_bibkg_scholar in entity:
            if entity[property_bibkg_scholar] in wikidata_scholar_dict:
                count_links += 1
                count_links_scholar += 1

        elif is_person:
            count_not_links += 1

print(count_url)
print("Total person: {}".format(count_person))
print("Total linked: {}".format(count_links))
print("Total not linked: {}".format(count_not_links))
print("Total linked with DBLP: {}".format(count_links_dblp))
print("Total linked with ORCID: {}".format(count_links_orcid))
print("Total linked with Scholar: {}".format(count_links_scholar))