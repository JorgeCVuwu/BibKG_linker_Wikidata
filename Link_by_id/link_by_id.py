import json
import re
import time
import os
import csv
from urllib.parse import urlparse

json_folder = "db/JSON/"
csv_folder = "db/CSV/"
carpeta_externa = "D:\Memoria" 
wikidata_scholar_name = "wikidata_scholar.json"
wikidata_person_name = "wikidata_person.json"
wikidata_else_name = "wikidata_else.json"

wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
bibkg_path = json_folder + "bibkg.json"
bibkg_linked_path = json_folder + "bibkg linked by id.json"
bibkg_link_sources_path = csv_folder + "bibkg link sources.csv"
wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)
wikidata_else_path = os.path.join(carpeta_externa, wikidata_else_name)

#publication properties
dblp_properties = ['P8978', 'P8926', 'P10692']
doi_property_w = 'P356'
arxiv_property_w = 'P818'
ieeexplore_property_w = 'P6480'
handle_property_w = 'P1184'
dnb_property_w = 'P1292'
acm_properties_w = ['P2179','P3332','P3333']
ethos_property_w = 'P4536'
isbn_properties = ['P957', 'P212']

#person properties
dblp_author_property = 'P2456'
orcid_property = 'P496'
google_scholar_property = 'P1960'


def detect_page(url):
    parsed_url = urlparse(url)

    if parsed_url.scheme in ["http", "https"]:
        page_prefix = parsed_url.scheme + "://" + parsed_url.netloc
        page_suffix = parsed_url.path.lstrip("/")
    else:
        page_prefix = ""
        page_suffix = url
    return page_prefix, page_suffix

def add_to_dict(dict, suffix, id):
    dict[suffix] = id

def process_dblp_url(entity, dblp_dict):
    #print(url)
    url = entity[':url'][0]['value']
    split = url.split('/')
    if split[0] != 'db':
        return False
    url1 = ''
    n = len(split) - 1
    for i in range(1, n):
        url1 += split[i] + '/'
    url_last = split[-1]
    if '#' in url_last:
        url_name =url_last.split('#')[1]
    else:
        url_name = url_last.replace(".html", "")
    dblp_id = url1 + url_name
     #dblp_dict[dblp_id] = id
    add_to_dict(dblp_dict, dblp_id, id)

def process_doi(id, ee, doi_dict):
    doi_prefix = 'doi.org/'
    doi_suffix = ee.split(doi_prefix, 1)[1]
    #doi_dict[doi_suffix] = id
    add_to_dict(doi_dict, doi_suffix.upper(), id)

def process_arxiv(id, ee, arxiv_dict):
    arxiv_prefix = 'arxiv.org/abs/'
    try:
        arxiv_suffix = ee.split(arxiv_prefix, 1)[1]
        #arxiv_dict[arxiv_suffix] = id
        add_to_dict(arxiv_dict, arxiv_suffix, id)
    except:
        pass

def process_ieeexplore(id, ee, ieee_dict):
    ieee_suffix = ee.split('/')[-2]
    #ieee_dict[ieee_suffix] = id
    add_to_dict(ieee_dict, ieee_suffix, id)

def process_handle(id, ee, handle_dict):
    handle_prefix = 'hdl.handle.net/'
    handle_suffix = ee.split(handle_prefix)[1]
    #handle_dict[handle_suffix] = id
    add_to_dict(handle_dict, handle_suffix, id)

def process_dnb(id, ee, dnb_dict):
    dnb_suffix = ee.split('/')[-1]
    #dnb_dict[dnb_suffix] = id
    add_to_dict(dnb_dict, dnb_suffix, id)

def process_acm(id, ee, acm_dict):
    acm_suffix = ee.split('=')[-1]
    #acm_dict[acm_suffix] = id
    add_to_dict(acm_dict, acm_suffix, id)

def process_ethos(id, ee, ethos_dict):
    ethos_suffix = ee.split('=')[-1]
    #ethos_dict[ethos_suffix] = id
    add_to_dict(ethos_dict, ethos_suffix, id)


def process_wikidata_dblp_author_id(id, entity, dblp_dict):
    key = entity['key']
    if key[:10] == "homepages/":
        id_sin_homepages = key[10:]
        add_to_dict(dblp_dict, id_sin_homepages, id)


def process_any(id, content, dict):
    add_to_dict(dict, content, id)

def link_by_id(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict = {}, bibkg_link_sources_path = bibkg_link_sources_path):

    doi_prefix = 'doi.org/'
    arxiv_prefix = 'arxiv.org/abs/'
    ieeexplore_prefix = 'ieeexplore.ieee.org/'
    handle_prefix = 'hdl.handle.net/'
    dnb_prefix = 'd-nb.info/'
    acm_prefix = 'dl.acm.org/'
    ethos_prefix = 'ethos.bl.uk/'


    doi_dict = {}
    arxiv_dict = {}
    dblp_dict = {}
    ieee_dict = {}
    handle_dict = {}
    dnb_dict = {}
    acm_dict = {}
    ethos_dict = {}
    isbn_dict = {}

    dblp_event_dict = {}
    dblp_venue_dict = {}
    dblp_publication_dict = {}

    dblp_person_dict = {}
    scholar_dict = {}
    orcid_dict = {}

    links_dict = {}

    count_links = 0
    count_relations = 0




    url_functions_dict = {doi_prefix:{'name':'DOI','function':process_doi, 'dict':doi_dict}, 
                        arxiv_prefix:{'name':'arXiv ID','function':process_arxiv, 'dict':arxiv_dict},
                        ieeexplore_prefix:{'name':'ieeeXplore','function':process_ieeexplore, 'dict':ieee_dict},
                        handle_prefix:{'name':'hdl.handle','function':process_handle, 'dict':handle_dict},
                        dnb_prefix:{'name':'d-nb.info','function':process_dnb, 'dict':dnb_dict},
                        acm_prefix:{'name':'ACM Classification Code','function':process_acm, 'dict':acm_dict},
                        ethos_prefix:{'name':'ethos','function':process_ethos, 'dict':ethos_dict}
                        }

    wikidata_properties_dict = {dblp_properties[0]:{'name':'DBLP publication ID','dict':dblp_dict,'filter-dict':dblp_publication_dict,'count-links':0, 'count-total':0}, 
                                dblp_properties[1]:{'name':'DBLP venue ID','dict':dblp_dict,'filter-dict':dblp_venue_dict,'count-links':0, 'count-total':0}, 
                                dblp_properties[2]:{'name':'DBLP event ID','dict':dblp_dict,'filter-dict':dblp_event_dict,'count-links':0, 'count-total':0}, 
                                doi_property_w:{'name':'DOI','dict':doi_dict,'count-links':0, 'count-total':0}, 
                                arxiv_property_w:{'name':'arXiv ID','dict':arxiv_dict,'count-links':0, 'count-total':0}, 
                                ieeexplore_property_w:{'name':'ieeeXplore','dict':ieee_dict,'count-links':0, 'count-total':0}, 
                                handle_property_w:{'name':'hdl.handle','dict':handle_dict,'count-links':0, 'count-total':0}, 
                                dnb_property_w:{'name':'d-nb.info','dict':dnb_dict,'count-links':0, 'count-total':0}, 
                                acm_properties_w[0]:{'name':'ACM Classification Code','dict':acm_dict,'count-links':0, 'count-total':0}, 
                                acm_properties_w[1]:{'name':'ACM Digital Library citation ID','dict':acm_dict,'count-links':0, 'count-total':0}, 
                                acm_properties_w[2]:{'name':'ACM Digital Library event ID','dict':acm_dict,'count-links':0, 'count-total':0}, 
                                ethos_property_w:{'name':'ethos','dict':ethos_dict,'count-links':0, 'count-total':0},
                                isbn_properties[0]:{'name':'ISBN-10','dict':isbn_dict,'count-links':0, 'count-total':0},
                                isbn_properties[1]:{'name':'ISBN-13','dict':isbn_dict,'count-links':0, 'count-total':0}}

    wikidata_properties_person_dict = {dblp_author_property:{'name':'DBLP author ID', 'dict':dblp_person_dict, 'count-links':0, 'count-total':0},
                                    orcid_property:{'name':'ORCID ID','dict':orcid_dict, 'count-links':0, 'count-total':0},
                                    google_scholar_property:{'name':'Google Scholar ID', 'dict':scholar_dict, 'count-links':0, 'count-total':0}}

    #leer BibKG y capturar los ee

    inicio = time.time()
    with open(bibkg_path, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if 'ee' in entity:
                ee = url_sin_prefijo = re.sub(r'^https?://', '', entity['ee'])
                for key in url_functions_dict:
                    if key in ee:
                        key_dict = url_functions_dict[key]
                        key_function = key_dict['function']
                        key_category_dict = key_dict['dict']
                        key_function(id, ee, key_category_dict)
                        break
            if ':url' in entity:
                process_dblp_url(entity, dblp_dict)
            if 'isbn' in entity:
                process_any(id, entity['isbn'], isbn_dict)
            if 'type' in entity and entity['type'] == 'Person':
                if 'scholar' in entity:
                    process_any(id, entity['scholar'], scholar_dict)
                if 'orcid' in entity:
                    process_any(id, entity['orcid'], orcid_dict)
                if 'key' in entity:
                    process_wikidata_dblp_author_id(id, entity, dblp_person_dict)


    print("IDs de BibKG cargados")
    print("Comparando con IDs de Wikidata")

    with open(wikidata_scholar_path, 'r') as wikidata_scholar:
        for linea in wikidata_scholar:
            entity = json.loads(linea)
            id = entity['id']
            claims = entity['claims'].items()
            for key, value in claims:
                if key in wikidata_properties_dict:
                    for valor in value:
                        try:
                            valor_at = valor['mainsnak']['datavalue']['value']
                        except:
                            continue
                        property = wikidata_properties_dict[key]
                        property_dict = property['dict']
                        if valor_at in property_dict:
                            property_id = property_dict[valor_at]
                            if 'filter-dict' in property:
                                wikidata_properties_dict[key]['filter-dict'][valor_at] = property_id
                            if property_id not in links_dict:
                                links_dict[property_id] = id
                                linked = True
                                count_links += 1 
                                property['count-links'] += 1
                            property['count-total'] += 1
                            count_relations += 1
                            break
                        elif property['name'] == 'DOI' and valor_at.upper() in property_dict:
                            property_id = property_dict[valor_at.upper()]
                            if property_id not in links_dict:
                                links_dict[property_id] = id
                                linked = True
                                count_links += 1 
                                property['count-links'] += 1
                            property['count-total'] += 1
                            count_relations += 1
                            break


    with open(wikidata_person_path, 'r') as wikidata_person:
        for linea in wikidata_person:
            entity = json.loads(linea)
            id = entity['id']
            claims = entity['claims'].items()
            for key, value in claims:
                if key in wikidata_properties_person_dict:
                    for valor in value:
                        try:
                            valor_at= valor['mainsnak']['datavalue']['value']
                        except:
                            continue
                        property = wikidata_properties_person_dict[key]
                        property_dict = property['dict']
                        if valor_at in property_dict:
                            property_id = property_dict[valor_at]
                            if property_id not in links_dict:
                                links_dict[property_id] = id
                                linked = True
                                count_links += 1 
                                property['count-links'] += 1
                            property['count-total'] += 1
                            count_relations += 1
                            break
                        # if key == property_dblp:
                        #     wikidata_dblp_dict[content] = id
                        # if key == property_orcid:
                        #     wikidata_orcid_dict[content] = id
                        # if key == property_scholar:
                        #     wikidata_scholar_dict[content] = id               
                                        
    print(len(links_dict))
    print("Escribiendo enlaces en BibKG")

    count_links_writed = 0

    wikidata_properties_dict.update(wikidata_properties_person_dict)

    #Invertir diccionarios para eficiencia de busqueda

    inverted_dicts_dict = {}

    for key, objects in wikidata_properties_dict.items():
        if 'filter-dict' in objects:
            diccionario_invertido = {valor: clave for clave, valor in wikidata_properties_dict[key]['filter-dict'].items()}
        else:
            diccionario_invertido = {valor: clave for clave, valor in wikidata_properties_dict[key]['dict'].items()}
        inverted_dicts_dict[objects['name']] = diccionario_invertido

    count_type_dict = {}

    with open(bibkg_path, 'r') as bibkg, open(bibkg_link_sources_path, mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        header_row = ['BibKG ID', 'Tipo']
        for name in inverted_dicts_dict:
            header_row.append(name)
        writer.writerow(header_row)

        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if 'type' in entity:
                entity_type = entity['type']
            else:
                entity_type = "unknown"
            if id in links_dict and 'wikidata' not in entity and id not in writed_links_dict:
                wikidata_id = links_dict[id]
                writed_links_dict[id] = wikidata_id
                del links_dict[id]
                count_links_writed += 1
                if entity_type not in count_type_dict:
                    count_type_dict[entity_type] = 0
                count_type_dict[entity_type] += 1
                csv_data.append([id, wikidata_id, 'linked_by_id'])

            row = [id,entity_type]
            for key, diccionarios in inverted_dicts_dict.items():
                if id in diccionarios:
                    row.append(diccionarios[id])
                else:
                    row.append('')
            writer.writerow(row)
            
                


    fin = time.time()

    print("Tiempo estimado del proceso: {} segundos".format(fin - inicio))

    # print("Lectura de Wikidata terminada")

    # print("Enlaces totales conseguidos: {}".format(count_links))
    # print("Relaciones entre entidades totales: {}".format(count_relations))
    # print("Enlaces de cada tipo:")
    # for key, value in wikidata_properties_dict.items():
    #     print("Enlaces conseguidos con {}: {}".format(value['name'], value['count-links']))
    #     print("Total de conexiones de BibKG con {}: {}".format(value['name'], value['count-total']))

    # # for key, value in wikidata_properties_person_dict.items():
    # #     print("Enlaces conseguidos con {}: {}".format(value['name'], value['count-links']))
    # #     print("Total de conexiones de BibKG con {}: {}".format(value['name'], value['count-total']))

    # print("Enlaces totales escritos en BibKG: {}".format(count_links_writed))


    #wikidata_properties_dict.update(wikidata_properties_person_dict)

    folder = 'Link_by_id/data/'
    metadata_path = folder + 'count-id-links-upper-doi.csv'
    type_count_path = folder + 'count-links-type.csv'

    #print("\nEscribiendo CSV de counts")

    with open(metadata_path, mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["ID", "Enlaces conseguidos", "Total de referencias en Wikidata"])
        sorted_items = sorted(wikidata_properties_dict.items(), key=lambda x: x[1]['count-total'], reverse=True)
        for llave, valor in sorted_items:
            writer.writerow([valor['name'], valor['count-links'], valor['count-total']])

    #print("\nEscribiendo CSV de counts de tipos")

    with open(type_count_path, mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["Tipo", "Count"])
        sorted_items = sorted(count_type_dict.items(), key=lambda x: x[1], reverse=True)
        for llave, valor in sorted_items:
            writer.writerow([llave, valor])

    #print("Proceso completado")

    return writed_links_dict, count_links_writed, csv_data

