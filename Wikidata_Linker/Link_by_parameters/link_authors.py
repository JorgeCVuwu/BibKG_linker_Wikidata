import json
import re
import time
import os
import csv

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg linked by id.json"
bibkg_names_path = json_folder + "bibkg_person_name.json"
bibkg_linked_path = json_folder + "bibkg linked authors.json"

carpeta_externa = "D:\Memoria" 
wikidata_person_name = "wikidata_person_4.json"
wikidata_scholar_name = "wikidata_scholar_4.json"

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
    return resultado.replace(".", "")

def process_author_id(id):
    if id[0:2] == "a_":
        return id[2:].replace("_", " ")

author_name_dict = {}
with open(bibkg_path, 'r') as bibkg:
    print("Almacenando autores de BibKG")
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'type' in entity:
            entity_type = entity['type']
            if entity_type == 'Person':
                author_name_dict[id] = entity['name']

def link_author(links_dict, bibkg_id, id, link_counts_dict, banlist_dict):
    if bibkg_id not in links_dict and bibkg_id not in banlist_dict:
        links_dict[bibkg_id] = id
    #Si una entidad es relacionada con otra entidad a la ya asociada, se elimina la asociación
    elif links_dict[bibkg_id] != id:
        banlist_dict[bibkg_id] = True
        del links_dict[bibkg_id]

    if bibkg_id not in link_counts_dict:
        link_counts_dict[bibkg_id] = {}
    if id not in link_counts_dict[bibkg_id]:
        link_counts_dict[bibkg_id][id] = 0
    link_counts_dict[bibkg_id][id] += 1


def link_authors(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict = {}, linked_method = "linked_by_id_propagation", author_name_dict = author_name_dict):
    print("Almacenando nombres de autores en \"author_of\"")

    inicio = time.time()

    bibkg_publications_dict = {}
    wikidata_person_dict = {}

    wikidata_author_property = 'P50'
    wikidata_author_string_property = 'P2093'

    links_dict = {}
    link_counts_dict = {}
    total_authors_bibkg_dict = {}
    string_authors_dict = {}

    count_links = 0
    count_author_index_error = 0
    count_wikidata_order = 0
    count_bibkg_order = 0
    count_orders = 0
    count_links_order = 0
    count_not_links_order = 0
    count_order_number_error = 0
    count_links_not_order = 0

    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if 'type' not in entity:
                continue
            type = entity['type']
            if ('wikidata' in entity or id in writed_links_dict) and 'has_author' in entity and type != 'Person':
                try:
                    wikidata_id = writed_links_dict[id]
                except:
                    wikidata_id = entity['wikidata']
                for author in entity['has_author']:
                    author_id = author['value']
                    try:
                        author['name'] = author_name_dict[author_id]
                    except:
                        author['name'] = process_author_id(author_id)
                bibkg_publications_dict[wikidata_id] = {'id':id,'has_author':entity['has_author']}

    del author_name_dict

    print("Leyendo personas de Wikidata")

    with open(wikidata_person_path, 'r') as wikidata_person:
        for linea in wikidata_person:
            entity = json.loads(linea)
            id = entity['id']
            if 'en' in entity['name']:
                wikidata_person_dict[id] = entity['name']['en']['value']
            else:
                for key, valor in entity['name'].items():
                    wikidata_person_dict[id] = valor['value']
                    break
            
    print("Comparando autores en Wikidata")

    c = 0
    break_condition = False
    with open(wikidata_scholar_path, 'r') as wikidata_scholar:
        banlist_dict = {}
        for linea in wikidata_scholar:
            entity = json.loads(linea)
            wikidata_id = entity['id']
            if wikidata_id in bibkg_publications_dict:
                bibkg_entity = bibkg_publications_dict[wikidata_id]
                claims = entity['claims']

                if wikidata_author_string_property in claims:
                    authors = claims[wikidata_author_string_property]
                    for author in authors:
                        if 'datavalue' in author['mainsnak']:
                            try:
                                wikidata_author_id = author['mainsnak']['datavalue']['value']
                                string_authors_dict[wikidata_author_id] = wikidata_author_id
                            except:
                                #print(author)
                                c+=1
                                # if c > 10:
                                #     break_condition = True
                                #     break
                                pass
                    pass
                if break_condition:
                    break
                if wikidata_author_property in claims:
                    authors = claims[wikidata_author_property]
                    author_names_list_bibkg = {}
                    order_list_bibkg = {}
                    for value in bibkg_entity['has_author']:
                        #Procesar nombre de BibKG
                        bibkg_person_id = value['value']
                        bibkg_person_name = value['name']
                        # print(bibkg_person_name)
                        # print(bibkg_person_id)
                        processed_name = process_names(bibkg_person_name)
                        author_names_list_bibkg[processed_name] = bibkg_person_id
                        if 'orden' in value:
                            order_list_bibkg[value['orden']] = processed_name
                        
                        if bibkg_person_id not in total_authors_bibkg_dict:
                            total_authors_bibkg_dict[bibkg_person_id] = processed_name
                    if len(order_list_bibkg) > 0:
                        count_bibkg_order += 1
                    #rint(author_names_list_bibkg)
                    #bibkg_publications_dict[wikidata_id]
                    # print(author_names_list_bibkg)
                    # print(authors)
                    
                    for author in authors:
                        #print(author)
                        count_order_errors = 0
                        if 'datavalue' in author['mainsnak']:
                            order_in_wikidata = True
                            wikidata_author_id = author['mainsnak']['datavalue']['value']
                            try:
                                wikidata_author_order = author['order']
                                count_orders += 1
                                #print("a")
                            except:
                                #print(author)
                                order_in_wikidata = False
                                count_order_errors += 1
                            #Procesar nombre de Wikidata
                            #print(author_name)
                            #print(wikidata_person_dict[author_value])
                            try:
                                wikidata_author_name = process_names(wikidata_person_dict[wikidata_author_id])
                            except:
                                count_author_index_error += 1
                                continue
                            #print(wikidata_author_name)
                            #print(author_names_list_bibkg)
                            #print(author_names_list_bibkg[wikidata_author_name])
                            
                            if order_in_wikidata:
                                try:
                                    name_order = order_list_bibkg[wikidata_author_order]
                                    if name_order in author_names_list_bibkg:
                                        bibkg_id = author_names_list_bibkg[name_order]
                                        link_author(links_dict, bibkg_id, id, link_counts_dict, banlist_dict)
                                        count_links+=1
                                        count_links_order += 1
                                    else:
                                        if wikidata_author_name in author_names_list_bibkg:
                                            bibkg_id = author_names_list_bibkg[wikidata_author_name]
                                            link_author(links_dict, bibkg_id, id, link_counts_dict, banlist_dict)
                                            count_links += 1
                                        count_not_links_order += 1
                                except:
                                    count_order_number_error += 1

                            else:
                                if wikidata_author_name in author_names_list_bibkg:
                                    bibkg_id = author_names_list_bibkg[wikidata_author_name]
                                    link_author(links_dict, bibkg_id, id, link_counts_dict, banlist_dict)
                                    count_links += 1
                                    count_links_not_order += 1

                    if order_in_wikidata:
                        count_wikidata_order += 1
                    #break

    count_repeated_id = 0
    count_links_dict = 0
    for key, lista in link_counts_dict.items():
        if len(lista) > 1:
            count_repeated_id += 1
        count_links_dict += 1

    count_links_writed = 0

    print("Verificando enlaces ya existentes en BibKG")

    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if id in links_dict and 'wikidata' not in entity and id not in writed_links_dict:
                wikidata_id = links_dict[id]
                writed_links_dict[id] = wikidata_id
                del links_dict[id]
                count_links_writed += 1
                csv_data.append([id, wikidata_id, linked_method])

    fin = time.time()
    # print("Guardando metadatos")

    # data = [
    #     ['time_hours', 'linked_entities', 'writed_linked_entities', 'total_author_entities_in_bibkg_publications', 'total_wikidata_string_authors'],
    #     [(fin - inicio)/3600, count_links_dict, count_links_writed, len(total_authors_bibkg_dict), len(string_authors_dict)]
    # ]
    # csv_folder = "Link by parameters/data/"
    # metadata_path = csv_folder + 'link-authors-metadata-2.csv'
    # with open(metadata_path, mode='w', newline='') as archivo_csv:
        
    #     # Crea el objeto de escritura de CSV
    #     writer = csv.writer(archivo_csv)
        
    #     # Escriba los datos en el archivo CSV
    #     for fila in data:
    #         writer.writerow(fila)
            

    # print("Total de publicaciones: {}".format(len(bibkg_publications_dict)))
    # print("Relaciones totales encontradas: {}".format(count_links))
    # print("Enlaces conectados sin considerar ya existentes: {}".format(count_links_dict))
    # print("Errores al encontrar al autor del has_author en Wikidata: {}".format(count_author_index_error))
    # print("Conteo de order en BibKG: {}".format(count_bibkg_order))
    # print("Conteo de order en Wikidata: {}".format(count_wikidata_order))
    # print("Conteo de errores de orden: {}".format(count_order_errors))
    # print("Conteo de autores con un orden asignado: {}".format(count_orders))
    # print("Total de strings de autores sin repetición: {}".format(len(string_authors_dict)))
    # print("Conteo de enlaces utilizando el parámetro de orden: {}".format(count_links_order))
    # print("Total de autores relacionados mediante orden, pero sin coincidir en los nombres: {}".format(count_not_links_order))
    # print("Errores de comparación con el número de orden: {}".format(count_order_number_error))
    # print("Total de autores de BibKG dentro de las entidades analizadas: {}".format(len(total_authors_bibkg_dict)))
    # print("Enlaces con más de 1 ID asociada: {}".format(count_repeated_id))
    # print("Enlaces sin utilizar el orden: {}".format(count_links_not_order))

    # print("Total de enlaces escritos: {}".format(count_links_writed))

    print("Tiempo de ejecución de link_authors: {} segundos".format(fin - inicio))

    return writed_links_dict, count_links_writed, csv_data


#link_authors(bibkg_path, wikidata_person_path, wikidata_scholar_path, [])
