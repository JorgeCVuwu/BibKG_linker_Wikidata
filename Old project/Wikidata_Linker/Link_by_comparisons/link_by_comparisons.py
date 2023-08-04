import json
import re
import time
import os
import csv
import traceback
from datetime import datetime
from dateutil import parser

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg linked authors.json"
bibkg_names_path = json_folder + "bibkg_person_name.json"
bibkg_linked_path = json_folder + "bibkg linked journals.json"

carpeta_externa = "D:\Memoria" 
wikidata_person_name = "wikidata_person_4.json"
wikidata_scholar_name = "wikidata_scholar_4.json"

wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

#get_year: -> str . acá, sólo se obtiene el año analizando los caracteres del 1 al 5, según el formato ISO 8601, por problemas al procesar 
# la fecha (de todos modos, el año siempre poseerá 4 dígitos (las entidades requeridas siempre tendrán una fecha posterior al siglo XIX))
def get_year(date):
    year = date[1:5]
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
    name = str(name)
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

    if 'first_property' not in global_dict: #
        global_dict['first_property'] = True #

    id = entity['id']
    property_dict_name = property + '_dict'
    if property_dict_name not in global_dict:
        global_dict[property_dict_name] = {}
    if property in entity:
        property_value = entity[property]
        if property == 'name':
            property_value = process_names(property_value)
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

    if 'first_author' not in global_dict: #
        global_dict['first_author'] = True #

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

        if global_dict['first_author']: #
            #print("Author de BibKG: {}".format(author_key)) #
            pass
        global_dict['first_author'] = False #

def compare_authors(entity, global_dict, bibkg_id):

    if 'authors_in' not in global_dict: #
        global_dict['authors_in'] = 0 #

    if 'first_author_w' not in global_dict: #
        global_dict['first_author_w'] = True #

    property = 'P50'
    author_string_property = 'P2093'
    claims = entity['claims']
    authors = ''
    authors_entities_dict = {}
    authors_string_dict = {}
    if 'count_authors_coincidences' not in global_dict:
        global_dict['count_authors_coincidences'] = 0
    if property in claims:
        authors_dict = claims[property]
        for author_object in authors_dict:
            if 'datavalue' in author_object['mainsnak']:
                author_id = author_object['mainsnak']['datavalue']['value']
                try:
                    author_value = process_names(global_dict['wikidata_person'][author_id])
                    author_order = author_object['order']
                    if author_order == 0:
                        pass
                        #print(author_object)
                    authors_entities_dict[author_order] = author_value
                except:
                    pass
                    #print(author_order)
                    #print(author_object)
                    #print(entity['id'])
                    #print(author_order)
                    #traceback.print_exc()
                #authors += author_value + '_' + str(author_order)
    if author_string_property in claims:
        authors_dict = claims[author_string_property]
        for author_object in authors_dict:
            if 'datavalue' in author_object['mainsnak']:
                author_value = process_names(author_object['mainsnak']['datavalue']['value'])
                try:            
                    author_order = author_object['order']
                    authors_string_dict[author_order] = author_value
                except:
                    pass
                    # print(author_object)
                    # print(entity)
                    # traceback.print_exc()
            #authors += author_value + '_' + str(author_order)
    #Se añaden las entidades de la propiedad string dict a las de la propiedad author, si es que no existe ya un orden similar.
    authors_entities_dict.update(authors_string_dict)
    authors_entities_dict = sorted(authors_entities_dict.items())
    for order, value in authors_entities_dict:
        if authors:
            authors += '##'
        authors += value + '_' + order

    if global_dict['first_author_w'] and (property in claims or author_string_property in claims): #
        #print(entity['claims']) #
        #print(entity['id']) #
        #print(authors_entities_dict) #
        #print(authors) #
        #print("Autores de Wikidata: {}".format(authors)) #
        global_dict['first_author_w'] = False #
    
    if authors in global_dict['author_dict']:
        authors_id = global_dict['author_dict'][authors]
        global_dict['authors_in'] += 1 #
        if bibkg_id in authors_id:
            global_dict['count_authors_coincidences'] += 1
            return True
        else:
            return False



def add_date(entity, global_dict):
    add_property(entity, global_dict, "year")

def compare_date(entity, global_dict, bibkg_id):

    if 'first_date' not in global_dict: #
        global_dict['first_date'] = True #

    date_property = 'P577'

    # if date_property in entity['claims'] and global_dict['first_date']: #
    #     print("Año de Wikidata: {}".format(entity['claims'][date_property])) #
    #     global_dict['first_date'] = False #


    if 'count_date_coincidences' not in global_dict:
        global_dict['count_date_coincidences'] = 0
    if date_property in entity['claims'] and 'datavalue' in entity['claims'][date_property][0]['mainsnak']:
        date_value = entity['claims'][date_property][0]['mainsnak']['datavalue']['value']['time']
        processed_year = get_year(date_value)

        if global_dict['first_date']: #
            pass
            #print("Año: {}".format(processed_year)) #
        global_dict['first_date'] = False #

        if processed_year in global_dict['year_dict']:
            id_list = global_dict['year_dict'][processed_year]
            if bibkg_id in id_list:
                global_dict['count_date_coincidences'] += 1
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
    add_property(entity, global_dict, 'url')

def compare_url(entity, global_dict):
    id = entity['id']
    return_id_list = set()
    official_website = 'P856'
    full_work_at_url = 'P953'
    if full_work_at_url in entity:
        property_value = entity[full_work_at_url]
        if property_value in global_dict['url_dict']:
            return_id_list.update(global_dict['url_dict'][property_value])
    if official_website in entity:
        property_value = entity[official_website]
        if property_value in global_dict['url_dict']:
            return_id_list.update(global_dict['url_dict'][property_value])

    return return_id_list

add_functions_list = [add_name, add_authors, add_date, add_url]
compare_functions_list = [compare_date, compare_authors]

def link_by_comparisons(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict = {}, add_functions_list= add_functions_list, compare_functions_list = compare_functions_list):

    inicio = time.time()

    links_dict = {}

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
    global_dict['count_total_entities'] = {}
    global_dict['count_entities_rep'] = {}
    count_total_entities = global_dict['count_total_entities']
    global_dict['count_entities_one_name'] = 0
    global_dict['count_names_id_list_up_zero'] = 0
    with open(wikidata_scholar_path, 'r') as wikidata_scholar:
        for linea in wikidata_scholar:
            entity = json.loads(linea)
            id = entity['id']
            names_id_list = compare_name(entity, global_dict)
            aliases_id_list = compare_aliases(entity, global_dict)
            url_id_list = compare_url(entity, global_dict)
            names_id_list.update(aliases_id_list)
            names_id_list.update(url_id_list)
            if len(names_id_list) == 1:
                global_dict['count_entities_one_name'] += 1
            total_entities = []
            n = len(names_id_list)
            if n not in global_dict['count_entities_rep']:
                global_dict['count_entities_rep'][n] = 0
            global_dict['count_entities_rep'][n] += 1
            if len(names_id_list) > 0:
                global_dict['count_names_id_list_up_zero'] += 1
                for name_id in names_id_list:
                    parameters_boolean = True
                    for compare_function in compare_functions_list:
                        if not compare_function(entity, global_dict, name_id):
                            parameters_boolean = False
                            break
                    if parameters_boolean:
                        total_entities.append(name_id)
            n_total_entities = len(total_entities)
            if n_total_entities not in count_total_entities:
                count_total_entities[n_total_entities] = 0
            count_total_entities[n_total_entities] += 1
            if n_total_entities == 1:
                links_dict[total_entities[0]] = id
                count_links += 1

    print("Analizando enlaces en BibKG")

    count_links_writed = 0

    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if id in links_dict and 'wikidata' not in entity:
                wikidata_id = links_dict[id]
                writed_links_dict[id] = wikidata_id
                csv_data.append([id, wikidata_id, 'linked_by_comparisons'])
                del wikidata_id
                count_links_writed += 1

    fin = time.time()

    print("Guardando metadatos")

    data = [
        ['time_hours', 'linked_entities'], #, 'writed_linked_entities'],
        [(fin - inicio)/3600, count_links] #, count_links_writed]
    ]
    csv_folder = "Link_by_comparisons/data/"
    metadata_path = csv_folder + 'link-comparisons-metadata.csv'
    with open(metadata_path, mode='w', newline='') as archivo_csv:
        
        # Crea el objeto de escritura de CSV
        writer = csv.writer(archivo_csv)
        
        # Escriba los datos en el archivo CSV
        for fila in data:
            writer.writerow(fila)

    print("Cantidad de entidades de Wikidata relacionadas con una misma entidad de BibKG: {}".format(count_total_entities))
    print("Relaciones totales encontradas entre entidades: {}".format(count_links))
    print("Coincidencias entre autores: {}".format(global_dict['count_authors_coincidences']))
    print("Coincidencias entre fechas (años): {}".format(global_dict['count_date_coincidences']))

    print("Total de combinaciones de autores relacionadas: {}".format(global_dict['authors_in']))
    print("Total de entidades de BibKG con exactamente una entidad con el mismo nombre en Wikidata: {}".format(global_dict['count_entities_one_name']))
    print("Total de entidades con más de una coincidencia entre nombres y aliases: {}".format(global_dict['count_names_id_list_up_zero']))
    #print(global_dict['count_entities_rep'])
    print("Tiempo de ejecución: {} segundos".format(fin - inicio))

    return writed_links_dict, count_links_writed, csv_data

#link_by_comparisons(bibkg_path, bibkg_linked_path, wikidata_person_path, wikidata_scholar_path, add_functions_list, compare_functions_list)
