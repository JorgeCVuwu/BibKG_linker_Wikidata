import json
import re
import time
import os
from urllib.parse import urlparse

json_folder = "db/JSON/"
carpeta_externa = "D:\Memoria" 
wikidata_scholar_name = "wikidata_scholar.json"
wikidata_else_name = "wikidata_else.json"

bibkg_path = json_folder + "bibkg.json"
bibkg_linked_path = json_folder + "bibkg linked by id.json"
wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)
wikidata_else_path = os.path.join(carpeta_externa, wikidata_else_name)

#publication, 
dblp_properties = ['P8978', 'P8926', 'P10692']
doi_property_w = 'P356'
arxiv_property_w = 'P818'
ieeexplore_property_w = 'P6480'
handle_property_w = 'P1184'
dnb_property_w = 'P1292'
acm_properties_w = ['P2179','P3332','P3333']
ethos_property_w = 'P4536'

scholarly_equivalent_properties = {'P496':'orcid', 'P1960':'scholar'}


person_equivalent_properties = {}

def detect_page(url):
    parsed_url = urlparse(url)

    if parsed_url.scheme in ["http", "https"]:
        page_prefix = parsed_url.scheme + "://" + parsed_url.netloc
        page_suffix = parsed_url.path.lstrip("/")
    else:
        page_prefix = ""
        page_suffix = url
    return page_prefix, page_suffix

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
    dblp_dict[dblp_id] = id

def process_doi(id, ee, doi_dict):
    doi_prefix = 'doi.org/'
    doi_suffix = ee.split(doi_prefix, 1)[1]
    doi_dict[doi_suffix] = id

def process_arxiv(id, ee, arxiv_dict):
    arxiv_prefix = 'arxiv.org/abs/'
    try:
        arxiv_suffix = ee.split(arxiv_prefix, 1)[1]
        arxiv_dict[arxiv_suffix] = id
    except:
        pass

def process_ieeexplore(id, ee, ieee_dict):
    ieee_suffix = ee.split('/')[-2]
    ieee_dict[ieee_suffix] = id

def process_handle(id, ee, handle_dict):
    handle_prefix = 'hdl.handle.net/'
    handle_suffix = ee.split(handle_prefix)[1]
    handle_dict[handle_suffix] = id

def process_dnb(id, ee, dnb_dict):
    dnb_suffix = ee.split('/')[-1]
    dnb_dict[dnb_suffix] = id

def process_acm(id, ee, acm_dict):
    acm_suffix = ee.split('=')[-1]
    acm_dict[acm_suffix] = id

def process_ethos(id, ee, ethos_dict):
    ethos_suffix = ee.split('=')[-1]
    ethos_dict[ethos_suffix] = id


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

links_dict = {}

count_links = 0


url_functions_dict = {doi_prefix:{'function':process_doi, 'dict':doi_dict}, 
                      arxiv_prefix:{'function':process_arxiv, 'dict':arxiv_dict},
                      ieeexplore_prefix:{'function':process_ieeexplore, 'dict':ieee_dict},
                      handle_prefix:{'function':process_handle, 'dict':handle_dict},
                      dnb_prefix:{'function':process_dnb, 'dict':dnb_dict},
                      acm_prefix:{'function':process_acm, 'dict':acm_dict},
                      ethos_prefix:{'function':process_ethos, 'dict':ethos_dict}}

wikidata_properties_dict = {dblp_properties[0]:{'name':'DBLP publication ID','dict':dblp_dict,'count':0}, 
                            dblp_properties[1]:{'name':'DBLP venue ID','dict':dblp_dict,'count':0}, 
                            dblp_properties[2]:{'name':'DBLP event ID','dict':dblp_dict,'count':0}, 
                            doi_property_w:{'name':'DOI','dict':doi_dict,'count':0}, 
                            arxiv_property_w:{'name':'arXiv ID','dict':arxiv_dict,'count':0}, 
                            ieeexplore_property_w:{'name':'ieeeXplore','dict':ieee_dict,'count':0}, 
                            handle_property_w:{'name':'hdl.handle','dict':handle_dict,'count':0}, 
                            dnb_property_w:{'name':'d-nb.info','dict':dnb_dict,'count':0}, 
                            acm_properties_w[0]:{'name':'ACM Classification Code','dict':acm_dict,'count':0}, 
                            acm_properties_w[1]:{'name':'ACM Digital Library citation ID','dict':acm_dict,'count':0}, 
                            acm_properties_w[2]:{'name':'ACM Digital Library event ID','dict':acm_dict,'count':0}, 
                            ethos_property_w:{'name':'ethos','dict':ethos_dict,'count':0}}

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
            processed_url = process_dblp_url(entity, dblp_dict)

print("IDs de BibKG cargados")
print("Comparando con IDs de Wikidata")

with open(wikidata_scholar_path, 'r') as wikidata_scholar:
    for linea in wikidata_scholar:
        entity = json.loads(linea)
        id = entity['id']
        claims = entity['claims']
        for key, value in claims.items():
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
                        if property_id not in links_dict:
                            links_dict[property_id] = id
                            linked = True
                            count_links += 1 
                        property['count'] += 1
                        break                
                                       
print(len(links_dict))
print("Escribiendo enlaces en BibKG")

count_links_writed = 0

# with open(bibkg_path, 'r') as bibkg, open(bibkg_linked_path, 'w') as bibkg_linked:
#     for linea in bibkg:
#         entity = json.loads(linea)
#         id = entity['id']
#         if id in links_dict and 'wikidata' not in entity:
#             wikidata_id = links_dict[id]
#             entity['wikidata'] = wikidata_id
#             count_links_writed += 1
#         json.dump(entity, bibkg_linked)
#         bibkg_linked.write("\n") 

fin = time.time()

print("Tiempo estimado del proceso: {} segundos".format(fin - inicio))

print("Lectura de Wikidata terminada")

print("Enlaces totales conseguidos: {}".format(count_links))
print("Enlaces de cada tipo:")
for key, value in wikidata_properties_dict.items():
    print("Enlaces conseguidos con {}: {}".format(value['name'], value['count']))

print("Enlaces totales escritos en BibKG: {}".format(count_links_writed))
