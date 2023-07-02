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
    return resultado.replace(".", "").lower()

def process_author_id(id):
    if id[0:2] == "a_":
        return id[2:].replace("_", " ")
    

def link_author(links_dict, bibkg_id, id, link_counts_dict):
    if bibkg_id not in links_dict:
        links_dict[bibkg_id] = id

    if bibkg_id not in link_counts_dict:
        link_counts_dict[bibkg_id] = {}
    if id not in link_counts_dict[bibkg_id]:
        link_counts_dict[bibkg_id][id] = 0
    link_counts_dict[bibkg_id][id] += 1

def link_publications(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict = {}, linked_method = "linked_by_id_propagation"):

    bibkg_publications_dict = {}
    wikidata_person_dict = {}

    wikidata_author_property = 'P50'

    links_dict = {}
    link_counts_dict = {}
    count_links = 0

    banlist = {}

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
                if entity_type == 'Person' and ('wikidata' in entity or id in writed_links_dict):
                    author_name_dict[id] = {'id':id, 'name':entity['name'], 'publications':{}}
                    try:
                        wikidata_id = entity['wikidata']
                    except:
                        wikidata_id = writed_links_dict[id] 
                    author_wikidata_id_dict[wikidata_id] = author_name_dict[id]
                    

    print("Almacenando publicaciones de BibKG en autores")

    count_author_publications = 0
    count_publications_linked_bibkg = 0
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
                        count_author_publications += 1
                        if 'wikidata' in entity:
                            count_publications_linked_bibkg += 1
                if break_c:
                    break

    print("Publicaciones añadidas a autores en BibKG: {}".format(count_author_publications))
    print("Publicaciones ya enlazadas con Wikidata: {}".format(count_publications_linked_bibkg))

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
                                    if 'aliases' in entity:
                                        author_entity['aliases'] = []
                                        for key, alias in entity['aliases'].items():
                                            for subalias in alias:
                                                alias_value = subalias['value']
                                                author_entity['aliases'].append(process_names(alias_value))

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
    count_links_name = 0
    count_links_alias = 0
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
                if 'name' in value and bibkg_name not in repeated_names: 
                    if bibkg_name == value['name']:
                        links_dict[bibkg_key] = wikidata_key
                        count_links_name += 1
                        count_links += 1
                    elif 'aliases' in bibkg_publication:
                        bibkg_aliases = bibkg_publication['aliases']
                        if value['name'] in bibkg_aliases:
                            if bibkg_key in links_dict and links_dict[bibkg_key] != wikidata_key:
                                banlist[bibkg_key] = True
                            links_dict[bibkg_key] = wikidata_key
                            count_links_alias += 1
                            count_links += 1                        

    print("Relaciones totales por nombre: {}".format(count_links_name))
    print("Relaciones totales por alias: {}".format(count_links_alias))

    print("Verificando enlaces ya existentes en BibKG")

    count_links_writed = 0
    count_already_linked = 0

    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if id in links_dict:
                if 'wikidata' not in entity and id not in writed_links_dict and id not in banlist:
                    wikidata_id = links_dict[id]
                    writed_links_dict[id] = wikidata_id
                    csv_data.append([id, wikidata_id, linked_method])
                    del links_dict[id]
                    count_links_writed += 1
                else:
                    count_already_linked += 1

    fin = time.time()
    # print("Guardando metadatos")

    # data = [
    #     ['time_hours', 'linked_entities', 'writed_linked_entities'],
    #     [(fin - inicio)/3600, count_links, count_links_writed]
    # ]
    # csv_folder = "Link by parameters/data/"
    # metadata_path = csv_folder + 'link-publications-metadata.csv'
    # with open(metadata_path, mode='w', newline='') as archivo_csv:
        
    #     # Crea el objeto de escritura de CSV
    #     writer = csv.writer(archivo_csv)
        
    #     # Escriba los datos en el archivo CSV
    #     for fila in data:
    #         writer.writerow(fila)
            

    print("Tiempo de ejecución de link_publications: {} segundos".format(fin - inicio))

    # print("Relaciones totales encontradas: {}".format(count_links))

    # print("Enlaces totales escritos en BibKG: {}".format(count_links_writed))

    # print("Entidades ya enlazadas previamente en BibKG: {}".format(count_already_linked))

    return writed_links_dict, count_links_writed, csv_data
            

#link_publications(bibkg_path, bibkg_linked_path, wikidata_person_path, wikidata_scholar_path)