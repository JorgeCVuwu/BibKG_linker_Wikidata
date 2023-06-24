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
wikidata_person_name = "wikidata_person_4.json"
wikidata_scholar_name = "wikidata_scholar_4.json"

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

def obtain_bibkg_authors(authors):
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

def process_author_id(id):
    if id[0:2] == "a_":
        return id[2:].replace("_", " ")

def add_property(entity, global_dict, property):
    id = entity['id']
    property_dict_name = property + '_dict'
    if property_dict_name not in global_dict:
        global_dict[property_dict_name] = {}
    if property in entity:
        property_value = entity[property]
        property_dict = global_dict[property_dict_name]
        if property_value not in property_dict:
            property_dict[property_value] = set()
        property_dict[property_value].add(id)

def add_name(entity, global_dict):
    add_property(entity, global_dict, "name")

def compare_name(entity, global_dict):
    return_id_list = set()
    wikidata_names = entity['name']
    for key, name_value in wikidata_names.items():
        processed_name = process_names(name_value['value'])
        if processed_name in global_dict['name_dict']:
            id_list = global_dict['name_dict'][processed_name]
            return_id_list.update(id_list)
    return return_id_list                

def compare_aliases(entity, global_dict):
    return_id_list = set()
    if 'aliases' in entity:
        aliases = entity['aliases']
        for alias_language, value in aliases.items():
            for alias_list in value:
                alias_value = process_names(alias_list['value'])
                try:
                    id_list = global_dict['name_dict'][alias_value]
                    return_id_list.update(id_list)
                except:
                    pass
    return return_id_list

def add_authors(entity, global_dict):
    id = entity['id']
    if 'author_dict' not in global_dict:
        global_dict['author_dict'] = {}
    if 'has_author' in entity:
        author_dict = global_dict['author_dict']
        author_key = ''
        first_author = True
        for author in entity['has_author']:
            if not first_author:
                author_key += '##'
            first_author = False
            author_value = author['value']
            if author_value in global_dict['person_dict']:
                author_key += process_names(global_dict['person_dict'][author_value])
            else:
                author_key += process_names(process_author_id(author_value))
            if 'orden' in author:
                orden = author['orden']
                author_key += '_' + str(orden)
        if author_key not in author_dict:
            author_dict[author_key] = set()
        author_dict[author_key].add(id)

def compare_authors(entity, global_dict, bibkg_id):
    property = 'P50'
    author_string_property = 'P2093'
    claims = entity['claims']
    authors = ''
    authors_entities_dict = {}
    authors_string_dict = {}
    if property in claims:
        authors_dict = claims[property]
        for author_object in authors_dict:
            author_id = author_object['mainsnak']['datavalue']['value']
            author_value = process_names(global_dict['wikidata_person'][author_id])
            try:
                author_order = author_object['order']
                if author_order == 0:
                    print(author_object)
            except:
                print(entity)
                print(author_object)
                traceback.print_exc()
            try:
                authors_entities_dict[author_order] = author_value
            except:
                #print(author_order)
                #print(author_object)
                print(entity['id'])
                print(author_order)
                traceback.print_exc()
            #authors += author_value + '_' + str(author_order)
    if author_string_property in claims:
        authors_dict = claims[author_string_property]
        for author_object in authors_dict:
            author_value = process_names(author_object['mainsnak']['datavalue']['value'])
            try:            
                author_order = author_object['order']
            except:
                print(author_object)
                print(entity)
                traceback.print_exc()
            authors_string_dict[author_order] = author_value
            #authors += author_value + '_' + str(author_order)
    #Se añaden las entidades de la propiedad string dict a las de la propiedad author, si es que no existe ya un orden similar.
    authors_entities_dict.update(authors_string_dict)
    authors_entities_dict = sorted(authors_entities_dict.items())
    for order, value in authors_entities_dict:
        if authors:
            authors += '##'
        authors += value + '_' + order

    if authors in global_dict['author_dict']:
        authors_id = global_dict['author_dict'][authors]
        if bibkg_id in authors_id:
            return True
        else:
            return False



def add_date(entity, global_dict):
    add_property(entity, global_dict, "year")

def compare_date(entity, global_dict, bibkg_id):
    date_property = 'P577'
    if date_property in entity['claims'] and 'datavalue' in entity['claims'][date_property][0]:
        date_value = entity['claims'][date_property][0]['datavalue']['value']['time']
        processed_year = get_year(date_value)
        if processed_year in global_dict['year_dict']:
            id_list = global_dict['year_dict'][processed_year]
            if bibkg_id in id_list:
                return True
            else:
                return False
    #Analizar esto
    return True   

def add_pages(entity, global_dict):
    add_property(entity, global_dict, "pages")

def add_in_journal(entity, global_dict):
    pass
    #add_property(entity, global_dict, "in_journal")

def add_url(entity, global_dict):
    pass

add_functions_list = [add_name, add_authors, add_date, add_pages]
compare_functions_list = [compare_date, compare_authors]

def link_by_comparisons(bibkg_path, bibkg_linked_path, wikidata_person_path, wikidata_scholar_path, add_functions_list, compare_functions_list):

    inicio = time.time()

    print("Almacenando personas de BibKG")

    global_dict = {'person_dict':{}}
    bibkg_person_dict = global_dict['person_dict']
    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if 'type' in entity:
                type = entity['type']
                if type == "Person":
                    bibkg_person_dict[id] = entity['name']


    print("Almacenando entidades de BibKG")

    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            for add_function in add_functions_list:
                add_function(entity, global_dict)
            #bibkg_entity_dict[id] = entity_dict

    del bibkg_person_dict

    print("Almacenando nombres de personas de Wikidata")

    global_dict['wikidata_person'] = {}
    wikidata_person_dict = global_dict['wikidata_person']

    with open(wikidata_person_path, 'r') as wikidata_person:
        for linea in wikidata_person:
            entity = json.loads(linea)
            id = entity['id']
            try:
                wikidata_person_dict[id] = next(iter(entity['name'].items()))[1]['value']
            except:
                #Entidades sin nombre
                #traceback.print_exc()
                pass
                #break
            

    print("Comparando con entidades de Wikidata")
    count_links = 0
    with open(wikidata_scholar_path, 'r') as wikidata_scholar:
        for linea in wikidata_scholar:
            entity = json.loads(linea)
            id = entity['id']
            names_id_list = compare_name(entity, global_dict)
            aliases_id_list = compare_aliases(entity, global_dict)
            names_id_list.update(aliases_id_list)
            total_entities = []
            if len(names_id_list) > 0:
                for name_id in names_id_list:
                    parameters_boolean = True
                    for compare_function in compare_functions_list:
                        if not compare_function(entity, global_dict, name_id):
                            parameters_boolean = False
                            break
                    if parameters_boolean:
                        total_entities.append(name_id)
            if len(total_entities) == 1:
                count_links += 1

    print(count_links)

link_by_comparisons(bibkg_path, bibkg_linked_path, wikidata_person_path, wikidata_scholar_path, add_functions_list, compare_functions_list)
