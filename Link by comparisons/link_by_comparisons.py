import json
import re
import time
import os
import csv
import traceback
from datetime import datetime

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg linked authors.json"
bibkg_names_path = json_folder + "bibkg_person_name.json"
bibkg_linked_path = json_folder + "bibkg linked journals.json"

carpeta_externa = "D:\Memoria" 
wikidata_person_name = "wikidata_person_3.json"
wikidata_scholar_name = "wikidata_scholar_3.json"

wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

def get_year(date):
    datetime_date = datetime.fromisoformat(date)
    year = datetime_date.year
    return year

def is_number(string):
    patron = r'^\d+$'
    if re.match(patron, string):
        return True
    else:
        return False

def obtain_authors(authors):
    authors_split = authors.split('##')
    for author_values in authors_split:
        author_parts = author_values.rsplit('_', 1)
        if author_parts[-1].isdigit():
            return (author_parts[0], author_parts[-1])
        else:
            return authors

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
    return resultado.replace(".", "").lower()

def add_property(entity, bibkg_dict, property):
    id = entity['id']
    property_dict_name = property + '_dict'
    if property_dict_name not in bibkg_dict:
        bibkg_dict[property_dict_name] = {}
    if property in entity:
        property_value = entity[property]
        property_dict = bibkg_dict[property_dict_name]
        if property_value not in property_dict:
            property_dict[property_value] = []
        property_dict[property_value].append(id)

def add_name(entity, bibkg_dict):
    add_property(entity, bibkg_dict, "name")

def compare_name(entity, bibkg_dict):
    wikidata_names = entity['name']
    for key, name_value in wikidata_names.items():
        processed_name = process_names(name_value)
        if processed_name in bibkg_dict['name_dict']:
            id_list = bibkg_dict['name_dict'][processed_name]

def add_authors(entity, bibkg_dict):
    id = entity['id']
    if 'has_author' in entity:
        author_key = ''
        first_author = True
        for author in entity['has_author']:
            if not first_author:
                author_key += '##'
                first_author = False
            author_value = author['value']
            author_key += process_names(bibkg_dict['person_dict'][author_value])
            if 'orden' in author:
                orden = author['orden']
                author_key += '_' + orden
        bibkg_dict[author_key] = id

def compare_authors(entity, bibkg_dict):
    property = 'P50'
    authors_dict = entity['claims'][property]
    for author_object in authors_dict:
        author_value = author_object['mainsnak']['datavalue']['value']
        

def add_date(entity, bibkg_dict):
    add_property(entity, bibkg_dict, "year")

def compare_date(entity, bibkg_dict):
    date_property = 'P577'
    date_value = entity['claims'][date_property][0]['datavalue']['value']['time']
    processed_year = get_year(date_value)
    if processed_year in bibkg_dict['year_dict']:
        id_list = bibkg_dict['year_dict'][processed_year]    

def add_pages(entity, bibkg_dict):
    add_property(entity, bibkg_dict, "pages")

def add_in_journal(entity, bibkg_dict):
    add_property(entity, bibkg_dict, "in_journal")

def add_url(entity, bibkg_dict):
    pass

add_functions_list = [add_name, add_authors, add_date, add_pages, add_in_journal]
compare_functions_list = []

def link_by_comparisons(bibkg_path, bibkg_linked_path, wikidata_person_path, wikidata_scholar_path, functions_list):

    inicio = time.time()

    print("Almacenando personas de BibKG")

    bibkg_dict = {}
    bibkg_person_dict = bibkg_dict['person_dict']
    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            type = entity['type']
            if type == "Person":
                bibkg_person_dict[id] = entity['name']


    print("Almacenando entidades de BibKG")

    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            for add_function in add_functions_list:
                add_function(entity, bibkg_dict)
            #bibkg_entity_dict[id] = entity_dict

    del bibkg_person_dict

    print("Almacenando nombres de personas de Wikidata")

    wikidata_person_dict = {}

    with open(wikidata_person_path, 'r') as wikidata_person:
        for linea in wikidata_person:
            entity = json.loads(linea)
            id = entity['id']
            wikidata_person_dict[id] = entity['name'][0]
            

    print("Comparando con entidades de Wikidata")

    with open(wikidata_scholar_path, 'r') as wikidata_scholar:
        for linea in wikidata_scholar:
            entity = json.loads(linea)
            id = entity['id']
            for compare_function in compare_functions_list:
                compare_function(entity, bibkg_dict)