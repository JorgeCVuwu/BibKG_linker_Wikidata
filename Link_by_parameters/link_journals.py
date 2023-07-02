import json
import re
import time
import os
import csv
import traceback

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg linked authors.json"
bibkg_names_path = json_folder + "bibkg_person_name.json"
bibkg_linked_path = json_folder + "bibkg linked journals.json"

carpeta_externa = "D:\Memoria" 
wikidata_person_name = "wikidata_person_3.json"
wikidata_scholar_name = "wikidata_scholar_3.json"

wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

def link_journals(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict = {}, linked_method = "linked_by_id_journal_propagation"):
    bibkg_publications_dict = {}
    wikidata_person_dict = {}

    wikidata_author_property = 'P50'
    wikidata_author_string_property = 'P2093'
    wikidata_published_in_property = 'P1433'

    links_dict = {}
    error_dict = {}
    error_dict_bibkg = {}


    count_links = 0
    count_links_writed = 0

    inicio = time.time()

    print("Cargando publicaciones de BibKG en memoria")

    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if 'in_journal' in entity:
                wikidata_id = ''
                if 'wikidata' in entity:
                    wikidata_id = entity['wikidata']
                elif id in writed_links_dict:
                    wikidata_id = writed_links_dict[id]
                entity_journal = entity['in_journal']
                if wikidata_id:    
                    bibkg_publications_dict[wikidata_id] = {'id':id,'in_journal':entity_journal}

    print("Comparando journals en Wikidata")

    c = 0
    count_errors = 0
    count_journal_errors = 0
    count_errors_bibkg = 0

    break_condition = False
    with open(wikidata_scholar_path, 'r') as wikidata_scholar:
        for linea in wikidata_scholar:
            entity = json.loads(linea)
            wikidata_id = entity['id']
            if wikidata_id in bibkg_publications_dict:
                bibkg_entity = bibkg_publications_dict[wikidata_id]
                claims = entity['claims']

                if wikidata_published_in_property in claims:
                    bibkg_journal_id = bibkg_entity['in_journal'][0]['value']
                    #print(bibkg_journal_id)
                    publishers = claims[wikidata_published_in_property]
                    n_publishers = len(publishers)
                    if n_publishers == 1:
                        for publisher in publishers:
                            if 'datavalue' in publisher['mainsnak']:
                                try:
                                    wikidata_journal_id = publisher['mainsnak']['datavalue']['value']
                                    if wikidata_journal_id in error_dict:
                                        error_dict[wikidata_journal_id] += 1
                                        count_journal_errors +=1
                                    if bibkg_journal_id not in links_dict:    
                                        links_dict[bibkg_journal_id] = wikidata_journal_id
                                        count_links += 1
                                        error_dict[wikidata_journal_id] = 1
                                        
                                    elif links_dict[bibkg_journal_id] != wikidata_journal_id:
                                        if bibkg_journal_id not in error_dict_bibkg:
                                            error_dict_bibkg[bibkg_journal_id] = 0
                                        error_dict_bibkg[bibkg_journal_id] += 1
                                        count_errors_bibkg += 1
                                    # elif links_dict[bibkg_journal_id] != wikidata_journal_id:
                                    #     print(wikidata_id)
                                    #     print(wikidata_journal_id)
                                    #     print(bibkg_journal_id + ' ' + links_dict[bibkg_journal_id])
                                    #     # break_condition = True
                                    #     # break
                                    # if break_condition:
                                    #     break
                                except Exception as e:
                                    count_errors+=1
                                    traceback.print_exc()
                    
                    pass


    print("Escribiendo enlaces en BibKG")


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
    print("Guardando metadatos")

    data = [
        ['time_hours', 'linked_entities', 'writed_linked_entities'],
        [(fin - inicio)/3600, count_links, count_links_writed]
    ]
    csv_folder = "Link by parameters/data/"
    metadata_path = csv_folder + 'link-journals-metadata.csv'
    # with open(metadata_path, mode='w', newline='') as archivo_csv:
        
    #     # Crea el objeto de escritura de CSV
    #     writer = csv.writer(archivo_csv)
        
    #     # Escriba los datos en el archivo CSV
    #     for fila in data:
    #         writer.writerow(fila)

    print("Total de entidades de Wikidata enlazados: {}".format(len(error_dict)))
    print("Total de enlaces encontrados: {}".format(count_links))        
    print("Total de enlaces escritos: {}".format(count_links_writed))
    print("Errores de datavalue de Wikidata: {}".format(count_errors))
    print("Errores de journals asociados a más de un ID de BibKG: {}".format(count_journal_errors))
    print("Errores de journals de BibKG asociados a más de un journal de Wikidata: {}".format(count_errors_bibkg))

    print("Tiempo estimado del proceso: {} segundos".format(fin - inicio))

    return writed_links_dict, count_links_writed, csv_data

#link_journals(bibkg_path, bibkg_linked_path, wikidata_person_path, wikidata_scholar_path)
