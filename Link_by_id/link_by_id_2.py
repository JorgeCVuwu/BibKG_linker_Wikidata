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

#class LinkByID(WikidataLinker):
class LinkByID():

    def __init__(self):
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

        self.wikidata_in_file = {}


        self.bibkg_link_sources_path = "data/wikidata_linker/bibkg link sources.csv"
        
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
                                        isbn_properties[1]:{'name':'ISBN-13','dict':self.isbn_dict,'count-links':0, 'count-total':0}}



    def process_dblp_url(self):
        #print(url)
        url = self.entity[':url'][0]['value']
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
        add_to_dict(self.dblp_dict, dblp_id, id)

    def process_doi(self, ee):
        doi_prefix = 'doi.org/'
        doi_suffix = ee.split(doi_prefix, 1)[1]
        #doi_dict[doi_suffix] = id
        add_to_dict(self.doi_dict, doi_suffix.upper(), self.id)

    def process_arxiv(self, ee):
        arxiv_prefix = 'arxiv.org/abs/'
        try:
            arxiv_suffix = ee.split(arxiv_prefix, 1)[1]
            #arxiv_dict[arxiv_suffix] = id
            add_to_dict(self.arxiv_dict, arxiv_suffix, self.id)
        except:
            pass

    def process_ieeexplore(self, ee):
        ieee_suffix = ee.split('/')[-2]
        #ieee_dict[ieee_suffix] = id
        add_to_dict(self.ieee_dict, ieee_suffix, self.id)

    def process_handle(self, ee):
        handle_prefix = 'hdl.handle.net/'
        handle_suffix = ee.split(handle_prefix)[1]
        #handle_dict[handle_suffix] = id
        add_to_dict(self.handle_dict, handle_suffix, self.id)

    def process_dnb(self, ee):
        dnb_suffix = ee.split('/')[-1]
        #dnb_dict[dnb_suffix] = id
        add_to_dict(self.dnb_dict, dnb_suffix, self.id)

    def process_acm(self, ee):
        acm_suffix = ee.split('=')[-1]
        #acm_dict[acm_suffix] = id
        add_to_dict(self.acm_dict, acm_suffix, self.id)

    def process_ethos(self, ee):
        ethos_suffix = ee.split('=')[-1]
        #ethos_dict[ethos_suffix] = id
        add_to_dict(self.ethos_dict, ethos_suffix, self.id)


    def process_wikidata_dblp_author_id(self):
        key = self.entity['key']
        if key[:10] == "homepages/":
            id_sin_homepages = key[10:]
            add_to_dict(self.dblp_dict, id_sin_homepages, self.id)


    def process_any(self, content, dict):
        add_to_dict(dict, content, self.id)

    def link_by_id(self, wikidata_linker):

        doi_prefix = 'doi.org/'
        arxiv_prefix = 'arxiv.org/abs/'
        ieeexplore_prefix = 'ieeexplore.ieee.org/'
        handle_prefix = 'hdl.handle.net/'
        dnb_prefix = 'd-nb.info/'
        acm_prefix = 'dl.acm.org/'
        ethos_prefix = 'ethos.bl.uk/'


        count_links = 0
        count_relations = 0

        #person properties
        dblp_author_property = 'P2456'
        orcid_property = 'P496'
        google_scholar_property = 'P1960'


        url_functions_dict = {doi_prefix:{'name':'DOI','function':self.process_doi}, 
                            arxiv_prefix:{'name':'arXiv ID','function':self.process_arxiv},
                            ieeexplore_prefix:{'name':'ieeeXplore','function':self.process_ieeexplore},
                            handle_prefix:{'name':'hdl.handle','function':self.process_handle},
                            dnb_prefix:{'name':'d-nb.info','function':self.process_dnb},
                            acm_prefix:{'name':'ACM Classification Code','function':self.process_acm},
                            ethos_prefix:{'name':'ethos','function':self.process_ethos}
                            }



        wikidata_properties_person_dict = {dblp_author_property:{'name':'DBLP author ID', 'dict':self.dblp_person_dict, 'count-links':0, 'count-total':0},
                                        orcid_property:{'name':'ORCID ID','dict':self.orcid_dict, 'count-links':0, 'count-total':0},
                                        google_scholar_property:{'name':'Google Scholar ID', 'dict':self.scholar_dict, 'count-links':0, 'count-total':0}}

        #leer BibKG y capturar los ee

        inicio = time.time()
        with open(wikidata_linker.bibkg_path, 'r') as bibkg:
            for linea in bibkg:
                self.entity = json.loads(linea)
                self.id = self.entity['id']
                if 'ee' in self.entity:
                    ee = re.sub(r'^https?://', '', self.entity['ee'])
                    for key in url_functions_dict:
                        if key in ee:
                            key_dict = url_functions_dict[key]
                            key_function = key_dict['function']
                            key_function(ee)
                            break
                if 'wikidata' in self.entity:
                    self.wikidata_in_file[self.id] = True
                if ':url' in self.entity:
                    self.process_dblp_url()
                if 'isbn' in self.entity:
                    self.process_any(self.entity['isbn'], self.isbn_dict)
                if 'type' in self.entity and self.entity['type'] == 'Person':
                    if 'scholar' in self.entity:
                        self.process_any(self.entity['scholar'], self.scholar_dict)
                    if 'orcid' in self.entity:
                        self.process_any(self.entity['orcid'], self.orcid_dict)
                    if 'key' in self.entity:
                        self.process_wikidata_dblp_author_id()


        print("IDs de BibKG cargados")
        print("Comparando con IDs de Wikidata")

        with open(wikidata_linker.wikidata_scholar_path, 'r') as wikidata_scholar:
            for linea in wikidata_scholar:
                self.entity = json.loads(linea)
                self.id = self.entity['id']
                claims = self.entity['claims'].items()
                for key, value in claims:
                    if key in self.wikidata_properties_dict:
                        for valor in value:
                            try:
                                valor_at = valor['mainsnak']['datavalue']['value']
                            except:
                                continue
                            property = self.wikidata_properties_dict[key]
                            property_dict = property['dict']
                            if valor_at in property_dict:
                                property_id = property_dict[valor_at]
                                if 'filter-dict' in property:
                                    self.wikidata_properties_dict[key]['filter-dict'][valor_at] = property_id
                                if property_id not in wikidata_linker.writed_links_dict and self.id not in self.wikidata_in_file:
                                    wikidata_linker.writed_links_dict[property_id] = self.id
                                    count_links += 1 
                                    property['count-links'] += 1
                                    wikidata_linker.csv_data.append([property_id, self.id, 'linked_by_id'])
                                property['count-total'] += 1
                                count_relations += 1
                                break
                            elif property['name'] == 'DOI' and valor_at.upper() in property_dict:
                                property_id = property_dict[valor_at.upper()]
                                if property_id not in wikidata_linker.writed_links_dict and self.id not in self.wikidata_in_file:
                                    wikidata_linker.writed_links_dict[property_id] = self.id
                                    count_links += 1 
                                    property['count-links'] += 1
                                    wikidata_linker.csv_data.append([property_id, self.id, 'linked_by_id'])
                                property['count-total'] += 1
                                count_relations += 1
                                break


        #Enlazar personas con el mismo ID
        with open(wikidata_linker.wikidata_person_path, 'r') as wikidata_person:
            for linea in wikidata_person:
                self.entity = json.loads(linea)
                self.id = self.entity['id']
                claims = self.entity['claims'].items()
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
                                if property_id not in wikidata_linker.writed_links_dict and self.id not in self.wikidata_in_file:
                                    wikidata_linker.writed_links_dict[property_id] = self.id
                                    count_links += 1 
                                    property['count-links'] += 1
                                    wikidata_linker.csv_data.append([property_id, self.id, 'linked_by_id'])
                                property['count-total'] += 1
                                count_relations += 1
                                break
                            # if key == property_dblp:
                            #     wikidata_dblp_dict[content] = id
                            # if key == property_orcid:
                            #     wikidata_orcid_dict[content] = id
                            # if key == property_scholar:
                            #     wikidata_scholar_dict[content] = id               
                                            
        print("Escribiendo enlaces en BibKG")

        count_links_writed = 0

        self.wikidata_properties_dict.update(wikidata_properties_person_dict)

        #Invertir diccionarios para eficiencia de busqueda

        inverted_dicts_dict = {}

        for key, objects in self.wikidata_properties_dict.items():
            if 'filter-dict' in objects:
                diccionario_invertido = {valor: clave for clave, valor in self.wikidata_properties_dict[key]['filter-dict'].items()}
            else:
                diccionario_invertido = {valor: clave for clave, valor in self.wikidata_properties_dict[key]['dict'].items()}
            inverted_dicts_dict[objects['name']] = diccionario_invertido

        count_type_dict = {}




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

        # folder = 'Link_by_id/data/'
        # metadata_path = folder + 'count-id-links-upper-doi.csv'
        # type_count_path = folder + 'count-links-type.csv'

        #print("\nEscribiendo CSV de counts")

        # with open(metadata_path, mode='w', newline='') as archivo_csv:
        #     writer = csv.writer(archivo_csv)
        #     writer.writerow(["ID", "Enlaces conseguidos", "Total de referencias en Wikidata"])
        #     sorted_items = sorted(self.wikidata_properties_dict.items(), key=lambda x: x[1]['count-total'], reverse=True)
        #     for llave, valor in sorted_items:
        #         writer.writerow([valor['name'], valor['count-links'], valor['count-total']])

        # #print("\nEscribiendo CSV de counts de tipos")

        # with open(type_count_path, mode='w', newline='') as archivo_csv:
        #     writer = csv.writer(archivo_csv)
        #     writer.writerow(["Tipo", "Count"])
        #     sorted_items = sorted(count_type_dict.items(), key=lambda x: x[1], reverse=True)
        #     for llave, valor in sorted_items:
        #         writer.writerow([llave, valor])

        #print("Proceso completado")

        

