import json
import re
import time
import os
import csv
from urllib.parse import urlparse

import sys

# # Obtén la ruta absoluta de la carpeta padre
# ruta_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# # Agrega la ruta padre al sys.path
# sys.path.append(ruta_padre)

#from ..wikidata_linker import WikidataLinker

def add_to_dict(dict, suffix, id):
    dict[suffix] = id

def detect_page(url):
    parsed_url = urlparse(url)

    if parsed_url.scheme in ["http", "https"]:
        page_prefix = parsed_url.scheme + "://" + parsed_url.netloc
        page_suffix = parsed_url.path.lstrip("/")
    else:
        page_prefix = ""
        page_suffix = url
    return page_prefix, page_suffix

def verify_substring(list, substring):
    element_list = []
    for element in list:
        if substring in element:
            element_list.append(element)
    return element_list

#get_dblp_url: extrae el ID de BibKG de una entidad, a partir de la propiedad 'url' (de existir las condiciones adecuadas)
def get_dblp_url(entity):
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
    return dblp_id

#class LinkByID(WikidataLinker):
class LinkByID():

    def __init__(self, wikidata_linker):

        self.wikidata_linker = wikidata_linker

        #Diccionario con los IDs de DBLP de cada entidad de BibKG (para ingresarlos a los CSV)
        self.dblp_ids_dict = {}

        self.doi_dict = {}
        self.arxiv_dict = {}
        self.dblp_dict = {}
        self.ieee_dict = {}
        self.handle_dict = {}
        self.dnb_dict = {}
        self.acm_dict = {}
        self.ethos_dict = {}
        self.isbn_dict = {}

        self.dblp_event_dict = {}
        self.dblp_venue_dict = {}
        self.dblp_publication_dict = {}

        self.dblp_person_dict = {}
        self.scholar_dict = {}
        self.orcid_dict = {}

        self.linked_property_dict = {}

        self.wikidata_in_file = {}

        self.wikidata_linked_id_entities = {}
        self.linked_properties_dict = {}

        self.isbn_links_dict = {}
        
        self.count_repeated_wikidata_entity = 0
        self.count_filtered_corr = 0
        self.count_duplicate_wikidata_links = 0
        self.count_duplicate_wikidata_links_id_linker = 0
        self.count_duplicate_wikidata_links_previously_linked = 0
        self.count_filtered_isbn = 0

        self.count_links = 0
        self.count_relations = 0

        doi_prefix = 'doi.org/'
        arxiv_prefix = 'arxiv.org/abs/'
        ieeexplore_prefix = 'ieeexplore.ieee.org/'
        handle_prefix = 'hdl.handle.net/'
        dnb_prefix = 'd-nb.info/'
        acm_prefix = 'dl.acm.org/'
        ethos_prefix = 'ethos.bl.uk/'

        #Diccionario de funciones de procesamiento de la ID relacionadas con cada propiedad (que permiten tener el mismo formato del ID
        # tanto en BibKG como en Wikidata)
        self.url_functions_dict = {doi_prefix:{'name':'DOI','function':self.process_doi}, 
                            arxiv_prefix:{'name':'arXiv ID','function':self.process_arxiv},
                            ieeexplore_prefix:{'name':'ieeeXplore','function':self.process_ieeexplore},
                            handle_prefix:{'name':'hdl.handle','function':self.process_handle},
                            dnb_prefix:{'name':'d-nb.info','function':self.process_dnb},
                            acm_prefix:{'name':'ACM Classification Code','function':self.process_acm},
                            ethos_prefix:{'name':'ethos','function':self.process_ethos}
                            }

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

        self.wikidata_properties_dict = {dblp_properties[0]:{'name':'DBLP publication ID','dict':self.dblp_dict,'filter-dict':self.dblp_publication_dict,'count-links':0, 'count-total':0}, 
                                        dblp_properties[1]:{'name':'DBLP venue ID','dict':self.dblp_dict,'filter-dict':self.dblp_venue_dict,'count-links':0, 'count-total':0}, 
                                        dblp_properties[2]:{'name':'DBLP event ID','dict':self.dblp_dict,'filter-dict':self.dblp_event_dict,'count-links':0, 'count-total':0}, 
                                        doi_property_w:{'name':'DOI','dict':self.doi_dict,'count-links':0, 'count-total':0}, 
                                        arxiv_property_w:{'name':'arXiv ID','dict':self.arxiv_dict,'count-links':0, 'count-total':0}, 
                                        ieeexplore_property_w:{'name':'ieeeXplore','dict':self.ieee_dict,'count-links':0, 'count-total':0}, 
                                        handle_property_w:{'name':'hdl.handle','dict':self.handle_dict,'count-links':0, 'count-total':0}, 
                                        dnb_property_w:{'name':'d-nb.info','dict':self.dnb_dict,'count-links':0, 'count-total':0}, 
                                        acm_properties_w[0]:{'name':'ACM Classification Code','dict':self.acm_dict,'count-links':0, 'count-total':0}, 
                                        acm_properties_w[1]:{'name':'ACM Digital Library citation ID','dict':self.acm_dict,'count-links':0, 'count-total':0}, 
                                        acm_properties_w[2]:{'name':'ACM Digital Library event ID','dict':self.acm_dict,'count-links':0, 'count-total':0}, 
                                        ethos_property_w:{'name':'ethos','dict':self.ethos_dict,'count-links':0, 'count-total':0},
                                        isbn_properties[0]:{'name':'ISBN-10','dict':self.isbn_dict,'count-links':0, 'count-total':0},
                                        isbn_properties[1]:{'name':'ISBN-13','dict':self.isbn_dict,'count-links':0, 'count-total':0},
                                        dblp_author_property:{'name':'DBLP author ID', 'dict':self.dblp_person_dict, 'count-links':0, 'count-total':0},
                                        orcid_property:{'name':'ORCID ID','dict':self.orcid_dict, 'count-links':0, 'count-total':0},
                                        google_scholar_property:{'name':'Google Scholar ID', 'dict':self.scholar_dict, 'count-links':0, 'count-total':0}
                                        }

        #Diccionario de valores asociados a las propiedades de personas
        # self.wikidata_properties_person_dict = {dblp_author_property:{'name':'DBLP author ID', 'dict':self.dblp_person_dict, 'count-links':0, 'count-total':0},
        #                                 orcid_property:{'name':'ORCID ID','dict':self.orcid_dict, 'count-links':0, 'count-total':0},
        #                                 google_scholar_property:{'name':'Google Scholar ID', 'dict':self.scholar_dict, 'count-links':0, 'count-total':0}}

        folder = 'data/wikidata_linker/'
        self.metadata_path = folder + 'count-id-links-test.csv'
        self.linked_id_csv_path = folder + 'id-links-corr.csv'
    #funciones process: ajustan el formato del string de la ID de BibKG de cada tipo para poder compararse con Wikidata

    def process_dblp_url(self, entity):
        dblp_id = get_dblp_url(entity)
        add_to_dict(self.dblp_dict, dblp_id, entity['id'])

    def process_doi(self, ee, id):
        doi_prefix = 'doi.org/'
        doi_suffix = ee.split(doi_prefix, 1)[1]
        #doi_dict[doi_suffix] = id
        add_to_dict(self.doi_dict, doi_suffix.upper(), id)

    def process_arxiv(self, ee, id):
        arxiv_prefix = 'arxiv.org/abs/'
        try:
            arxiv_suffix = ee.split(arxiv_prefix, 1)[1]
            #arxiv_dict[arxiv_suffix] = id
            add_to_dict(self.arxiv_dict, arxiv_suffix, id)
        except:
            pass

    def process_ieeexplore(self, ee, id):
        ieee_suffix = ee.split('/')[-2]
        #ieee_dict[ieee_suffix] = id
        add_to_dict(self.ieee_dict, ieee_suffix, id)

    def process_handle(self, ee, id):
        handle_prefix = 'hdl.handle.net/'
        handle_suffix = ee.split(handle_prefix)[1]
        #handle_dict[handle_suffix] = id
        add_to_dict(self.handle_dict, handle_suffix, id)

    def process_dnb(self, ee, id):
        dnb_suffix = ee.split('/')[-1]
        #dnb_dict[dnb_suffix] = id
        add_to_dict(self.dnb_dict, dnb_suffix, id)

    def process_acm(self, ee, id):
        acm_suffix = ee.split('=')[-1]
        #acm_dict[acm_suffix] = id
        add_to_dict(self.acm_dict, acm_suffix, id)

    def process_ethos(self, ee, id):
        ethos_suffix = ee.split('=')[-1]
        #ethos_dict[ethos_suffix] = id
        add_to_dict(self.ethos_dict, ethos_suffix, id)


    def process_wikidata_dblp_author_id(self, entity, id):
        key = entity['key']
        if key[:10] == "homepages/":
            id_sin_homepages = key[10:]
            add_to_dict(self.dblp_person_dict, id_sin_homepages, id)


    def process_any(self, content, dict, id):
        add_to_dict(dict, content, id)

    #link_entities: enlaza entidades guardándolas en la tabla para el CSV, y almacena datos del enlazamiento
    def link_entities(self, property_id, id, key, valor_at):
            property_name = self.wikidata_properties_dict[key]['name']
            writed_links_dict = self.wikidata_linker.writed_links_dict
            writed_links_dict[property_id] = id
            dblp_id = self.dblp_ids_dict.get(property_id)
            if not dblp_id:
                dblp_id = ''
            self.wikidata_linker.csv_data.setdefault(property_id, [id, dblp_id])
            self.wikidata_linker.csv_data[property_id].append('linked_by_id')
            #self.wikidata_linker.csv_data.append([property_id, id, 'linked_by_id'])
            # if property_id in self.linked_properties_dict: #
            #     i = 2
            #     while True:
            #         repeated_property_id = property_id + '###' + str(i)
            #         if repeated_property_id not in self.linked_properties_dict:
            #             property_id = repeated_property_id
            #             break
            #         i += 1 #
            self.linked_properties_dict.setdefault(property_id, {'wikidata-id':id, 'first-property-linker':key})
            self.linked_properties_dict[property_id][property_name] = valor_at
            if property_name == 'ISBN-10' or property_name == 'ISBN-13':
                self.isbn_links_dict[id] = property_id

    #write_data_csv: escribe los enlaces de cada entidad de BibKG con Wikidata, junto con las fuentes de datos enlazadas y sus valores de IDs
    def write_id_linked_entities(self):
        with open(self.linked_id_csv_path, mode='w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            csv_id_data = ['bibkg_id', 'wikidata_id', 'dblp_id']
            for key, property in self.wikidata_properties_dict.items():
                csv_id_data.append(property['name'])
            writer.writerow(csv_id_data)
            for key, value in self.linked_properties_dict.items():
                #En este caso, si el ID no se encuentra "prohibido", se almacena como enlace
                if key not in self.wikidata_linker.forbidden_links_dict:
                    self.wikidata_linker.writed_id_entities[key] = True
                    row = [key, value['wikidata-id']]

                    dblp_id = self.dblp_ids_dict.get(key)
                    if dblp_id:
                        row.append(dblp_id)
                    else:
                        row.append('')
                    first_property_key = value['first-property-linker']
                    self.wikidata_properties_dict[first_property_key]['count-links'] += 1
                    for key, property in self.wikidata_properties_dict.items():
                        if property['name'] in value:
                            row.append(value[property['name']])
                            property['count-total'] += 1
                        else:
                            row.append('')
                    writer.writerow(row)
        
    #write_count_data_csv: Escribe los conteos del proceso (conteos de cada tipo de enlace y de cada referencia encontrada)
    def write_count_data_csv(self, time):
        with open(self.metadata_path, mode='w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(["ID", "Enlaces conseguidos", "Total de referencias en Wikidata"])
            sorted_items = sorted(self.wikidata_properties_dict.items(), key=lambda x: x[1]['count-total'], reverse=True)
            for _, valor in sorted_items:
                writer.writerow([valor['name'], valor['count-links'], valor['count-total']])
        


    #link_by_id: Relaciona a las entidades equivalentes entre BibKG y Wikidata mediante comparación de IDs, y guarda la información en
    # WikidataLinker 
    def link_by_id(self):
        
        #leer BibKG y capturar los ee

        inicio = time.time()
        with open(self.wikidata_linker.bibkg_path, 'r') as bibkg:
            for linea in bibkg:
                entity = json.loads(linea)
                id = entity['id']

                if 'key' in entity:
                    self.dblp_ids_dict[id] = entity['key']
                elif 'url' in entity:
                    dblp_id = get_dblp_url(entity)
                    if dblp_id:
                        self.dblp_ids_dict[id] = dblp_id


                if 'ee' in entity:
                    ee = re.sub(r'^https?://', '', entity['ee'])
                    for key in self.url_functions_dict:
                        if key in ee:
                            key_dict = self.url_functions_dict[key]
                            key_function = key_dict['function']
                            key_function(ee, id)
                            break
                if 'wikidata' in entity:
                    self.wikidata_in_file[entity['wikidata']] = id
                if ':url' in entity:
                    self.process_dblp_url(entity)
                if 'isbn' in entity:
                    self.process_any(entity['isbn'], self.isbn_dict, id)
                if 'type' in entity and entity['type'] == 'Person':
                    if 'scholar' in entity:
                        self.process_any(entity['scholar'], self.scholar_dict, id)
                    if 'orcid' in entity:
                        self.process_any(entity['orcid'], self.orcid_dict, id)
                    if 'key' in entity:
                        self.process_wikidata_dblp_author_id(entity, id)


        print("IDs de BibKG cargados")
        print("Comparando con IDs de Wikidata")

        with open(self.wikidata_linker.wikidata_scholar_path, 'r') as wikidata_scholar:
            for linea in wikidata_scholar:
                entity = json.loads(linea)
                id = entity['id']
                claims = entity['claims'].items()
                for key, value in claims:
                    if key in self.wikidata_properties_dict:
                        for valor in value:
                            try:
                                valor_at = valor['mainsnak']['datavalue']['value']
                            except:
                                continue
                            property = self.wikidata_properties_dict[key]
                            property_name = property['name']
                            property_dict = property['dict']
                            entity_rank = valor.get('rank')
                            #verifica que el valor de la propiedad no posea el status 'deprecated' (o sea, que Wikidata considera un valor incorrecto)
                            if entity_rank != 'deprecated':
                                #Si el valor de la propiedad de Wikidata está almacenado en el diccionario respectivo de BibKG
                                if valor_at and valor_at in property_dict:
                                    property_id = property_dict[valor_at]
                                    if 'filter-dict' in property:
                                        self.wikidata_properties_dict[key]['filter-dict'][valor_at] = property_id
                                    if property_id not in self.wikidata_linker.writed_links_dict and id not in self.wikidata_in_file:   
                                        wikidata_linked_entities = self.wikidata_linked_id_entities        
                                        if id not in wikidata_linked_entities:
                                            self.link_entities(property_id, id, key, valor_at)
                                            wikidata_linked_entities[id] = [property_id]

                                        else:
                                            if '_corr_' in property_id:
                                                self.count_filtered_corr += 1
                                                pass
                                            elif property_name == 'ISBN-10' or property_name == 'ISBN-13':
                                                self.count_filtered_isbn += 1
                                                pass
                                            else:
                                                #self.link_entities(property_id, id, property_name, valor_at)
                                                #wikidata_linked_entities[id].append(property_id)
                                                self.count_repeated_wikidata_entity += 1
                                                for bibkg_id in wikidata_linked_entities[id]:
                                                    self.wikidata_linker.forbidden_links_dict[bibkg_id] = True
                                    #Agregar ID de la fuente enlazamiento, en caso de que ya estuviera enlazado
                                    elif self.wikidata_linker.writed_links_dict.get(property_id) == id:
                                        self.linked_properties_dict[property_id][property_name] = valor_at
                                    #revisar enlaces repetidos
                                    else:
                                        if property_id in self.wikidata_linker.writed_links_dict and self.wikidata_linker.writed_links_dict[property_id] != id:
                                        #if self.wikidata_linker.writed_links_dict.get(property_id) != id:
                                            self.count_duplicate_wikidata_links += 1
                                            self.count_duplicate_wikidata_links_id_linker += 1
                                            #self.link_entities(property_id, id, property_name, valor_at)

                                            if self.count_duplicate_wikidata_links_id_linker < 10:
                                                print(id)
                                                print(property_id)
                                                print(self.wikidata_linker.writed_links_dict[property_id])

                                        if id in self.wikidata_in_file and self.wikidata_in_file[id] != property_id:
                                        #elif self.wikidata_in_file.get(id) != property_id:
                                            self.count_duplicate_wikidata_links += 1
                                            self.count_duplicate_wikidata_links_previously_linked += 1
                                                                                      

                                    #property['count-total'] += 1
                                    self.count_relations += 1
                                    break
                                #Si la propiedad es DOI
                                elif property_name == 'DOI' and valor_at.upper() in property_dict:
                                    property_id = property_dict[valor_at.upper()]
                                    if property_id not in self.wikidata_linker.writed_links_dict and id not in self.wikidata_in_file:
                                        wikidata_linked_entities = self.wikidata_linked_id_entities
                                        if id not in wikidata_linked_entities:
                                            self.link_entities(property_id, id, key, valor_at)
                                            wikidata_linked_entities[id] = [property_id]
                                        #Agregar ID de la fuente enlazamiento, en caso de que ya estuviera enlazado
                                        elif self.wikidata_linker.writed_links_dict.get(property_id) == id:
                                            self.linked_properties_dict[property_id][property_name] = valor_at
                                        else:
                                            corr_ids = verify_substring(wikidata_linked_entities[id], '_corr_')
                                            self.link_entities(property_id, id, key, valor_at) #
                                            if id in self.isbn_links_dict:
                                                self.wikidata_linker.forbidden_links_dict[self.isbn_links_dict[id]] = True
                                                self.isbn_links_dict.remove(id)
                                            if corr_ids:
                                                for corr_id in corr_ids:
                                                    self.wikidata_linker.forbidden_links_dict[corr_id] = True
                                                    wikidata_linked_entities[id].remove(corr_id)
                                            else:
                                                #wikidata_linked_entities[id].append(property_id) #
                                                self.count_repeated_wikidata_entity += 1
                                                for bibkg_id in wikidata_linked_entities[id]:
                                                    self.wikidata_linker.forbidden_links_dict[bibkg_id] = True
                                    #revisar enlaces repetidos
                                    else:
                                        if property_id in self.wikidata_linker.writed_links_dict and self.wikidata_linker.writed_links_dict[property_id] != id:
                                        #if self.wikidata_linker.writed_links_dict.get(property_id) != id:
                                            self.count_duplicate_wikidata_links += 1
                                            self.count_duplicate_wikidata_links_id_linker += 1
                                            #self.link_entities(property_id, id, property_name, valor_at)
                                        if id in self.wikidata_in_file and self.wikidata_in_file[id] != property_id:
                                        #elif self.wikidata_in_file.get(id) != property_id:
                                            self.count_duplicate_wikidata_links += 1
                                            self.count_duplicate_wikidata_links_previously_linked += 1                                                   

                                    #property['count-total'] += 1
                                    self.count_relations += 1
                                    break

        #Enlazar personas con el mismo ID
        with open(self.wikidata_linker.wikidata_person_path, 'r') as wikidata_person:
            for linea in wikidata_person:
                entity = json.loads(linea)
                id = entity['id']
                claims = entity['claims'].items()
                for key, value in claims:
                    if key in self.wikidata_properties_dict:
                        for valor in value:
                            try:
                                valor_at = valor['mainsnak']['datavalue']['value']
                            except:
                                continue
                            property = self.wikidata_properties_dict[key]
                            property_dict = property['dict']
                            property_name = property['name']
                            entity_rank = valor.get('rank')
                            if entity_rank != 'deprecated':
                                wikidata_linked_entities = self.wikidata_linked_id_entities
                                if valor_at in property_dict:
                                    property_id = property_dict[valor_at]
                                    if property_id not in self.wikidata_linker.writed_links_dict and id not in self.wikidata_in_file:

                                        if id not in wikidata_linked_entities: ####
                                            self.link_entities(property_id, id, key, valor_at)####
                                        else:
                                            self.count_repeated_wikidata_entity += 1
                                            for bibkg_id in wikidata_linked_entities[id]:
                                                self.wikidata_linker.forbidden_links_dict[bibkg_id] = True                                            
                                        wikidata_linked_entities[id] = [property_id]
                                    elif self.wikidata_linker.writed_links_dict.get(property_id) == id:
                                        self.linked_properties_dict[property_id][property_name] = valor_at
                                    #revisar enlaces repetidos
                                    else:
                                        if self.wikidata_linker.writed_links_dict.get(property_id) != id:
                                            self.count_duplicate_wikidata_links += 1
                                            self.count_duplicate_wikidata_links_id_linker += 1
                                            #self.link_entities(property_id, id, property_name, valor_at)
                                        elif self.wikidata_in_file.get(id) != property_id:
                                            self.count_duplicate_wikidata_links += 1
                                            self.count_duplicate_wikidata_links_previously_linked += 1  
                                    #property['count-total'] += 1
                                    self.count_relations += 1
                                    break
             
        print("Escribiendo enlaces en BibKG")

        count_links_writed = 0

        #self.wikidata_properties_dict.update(self.wikidata_properties_person_dict)

        

        fin = time.time()

        tiempo = fin - inicio

        self.write_id_linked_entities()
        self.write_count_data_csv(tiempo)

        print("IDs con _corr filtrados de enlazamiento: {}".format(self.count_filtered_corr))
        print("IDs de BibKG con entidades repetidas de Wikidata enlazados: {}".format(self.count_repeated_wikidata_entity))

        print("Enlaces con ISBN filtrados: {}".format(self.count_filtered_isbn))
        print("Entidades de BibKG relacionadas con más de 1 entidad de Wikidata: {}".format(self.count_duplicate_wikidata_links))
        print("Duplicaciones por el método de enlaces por IDs: {}".format(self.count_duplicate_wikidata_links_id_linker))
        print("Duplicaciones con respecto al enlace creado previamente: {}".format(self.count_duplicate_wikidata_links_previously_linked))

        print("Tiempo estimado del proceso: {} segundos".format(fin - inicio))

        # print("Lectura de Wikidata terminada")

        # print("Enlaces totales conseguidos: {}".format(count_links))
        # print("Relaciones entre entidades totales: {}".format(count_relations))
        # # print("Enlaces de cada tipo:")
        # for key, value in self.wikidata_properties_dict.items():
        #     print("Enlaces conseguidos con {}: {}".format(value['name'], value['count-links']))
        #     print("Total de conexiones de BibKG con {}: {}".format(value['name'], value['count-total']))

        # for key, value in wikidata_properties_person_dict.items():
        #     print("Enlaces conseguidos con {}: {}".format(value['name'], value['count-links']))
        #     print("Total de conexiones de BibKG con {}: {}".format(value['name'], value['count-total']))

        # print("Enlaces totales escritos en BibKG: {}".format(count_links_writed))


        # self.wikidata_properties_dict.update(wikidata_properties_person_dict)



        

