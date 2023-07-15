#author
import json
import re
import time
import os
import csv

def is_number(string):
    patron = r'^\d+$'
    if re.match(patron, string):
        return True
    else:
        return False

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

class LinkByParameters():

    def __init__(self, wikidata_linker):

        self.wikidata_linker = wikidata_linker

        self.dblp_ids_dict = {}

        self.bibkg_publications_dict = {}
        self.wikidata_person_dict = {}
        self.string_authors_dict = {}
        self.bibkg_author_dict = {}
        self.author_wikidata_id_dict = {}
        self.parameters_links = {}

        #Propiedades de Wikidata
        self.wikidata_author_property = 'P50'
        self.wikidata_author_string_property = 'P2093'
        self.wikidata_published_in_property = 'P1433'

        self.count_links = 0
        self.count_publication_links = 0
        self.count_author_links = 0
        self.count_journal_links = 0

        self.count_publication_relations = 0

        self.count_fordidden_author = 0
        self.count_fordidden_publication = 0
        self.count_fordidden_journal = 0

    #link_authors: si se cumplen las condiciones, enlaza entidades de autores de BibKG y Wikidata
    def link_authors(self, bibkg_id, wikidata_id):
        writed_links_dict = self.wikidata_linker.writed_links_dict
        forbidden_links_dict = self.wikidata_linker.forbidden_links_dict
        if bibkg_id not in writed_links_dict: 
            if bibkg_id not in forbidden_links_dict:
                writed_links_dict[bibkg_id] = wikidata_id
                self.count_links += 1
                self.count_author_links += 1
                dblp_id = self.dblp_ids_dict.get(bibkg_id)
                if not dblp_id:
                    dblp_id = ''
                self.wikidata_linker.csv_data.setdefault(bibkg_id, [wikidata_id, dblp_id])
                self.wikidata_linker.csv_data[bibkg_id].append('linked_by_{}_recursion_authors'.format(self.link_type))
                #self.wikidata_linker.csv_data.append([bibkg_id, wikidata_id, 'linked_by_{}_recursion_authors'.format(self.link_type)])
        #Si una entidad es relacionada con otra entidad a la ya asociada, se elimina la asociación
        elif writed_links_dict[bibkg_id] != wikidata_id:
            #Si el elemento no está escrito por el enlazamiento por IDs, pasa a la lista prohibida y elimina el enlace actual
            if bibkg_id not in self.wikidata_linker.writed_id_entities:
                forbidden_links_dict[bibkg_id] = True
                del writed_links_dict[bibkg_id]
                self.count_fordidden_author += 1
            
            #De lo contrario, no se hace nada en este punto
        else:
            self.wikidata_linker.csv_data[bibkg_id].append('linked_by_{}_recursion_authors'.format(self.link_type))

    #link_authors: si se cumplen las condiciones, enlaza entidades de publicaciones (y entidades con autores en general) de BibKG y Wikidata
    def link_publications(self, bibkg_id, wikidata_id):
        writed_links_dict = self.wikidata_linker.writed_links_dict
        forbidden_links_dict = self.wikidata_linker.forbidden_links_dict
        if bibkg_id not in writed_links_dict:
            if bibkg_id not in forbidden_links_dict:
                writed_links_dict[bibkg_id] = wikidata_id
                self.count_links += 1
                self.count_publication_links += 1
                dblp_id = self.dblp_ids_dict.get(bibkg_id)
                if not dblp_id:
                    dblp_id = ''
                self.wikidata_linker.csv_data.setdefault(bibkg_id, [wikidata_id, dblp_id])
                self.wikidata_linker.csv_data[bibkg_id].append('linked_by_{}_recursion_publications'.format(self.link_type))
                #self.wikidata_linker.csv_data.append([bibkg_id, wikidata_id, 'linked_by_{}_recursion_publications'.format(self.link_type)])        
        elif writed_links_dict[bibkg_id] != wikidata_id:
            # print("a: {}".format(bibkg_id))
            # print("b: {}".format(wikidata_id))
            # print("c: {}".format(writed_links_dict[bibkg_id]))
            if bibkg_id not in self.wikidata_linker.writed_id_entities:
                forbidden_links_dict[bibkg_id] = True
                del writed_links_dict[bibkg_id]
                self.count_fordidden_publication += 1
        else:
            self.wikidata_linker.csv_data[bibkg_id].append('linked_by_{}_recursion_publications'.format(self.link_type))    

    #link_authors: si se cumplen las condiciones, enlaza entidades de revistas de BibKG y Wikidata
    def link_journals(self, bibkg_id, wikidata_id):
        writed_links_dict = self.wikidata_linker.writed_links_dict
        forbidden_links_dict = self.wikidata_linker.forbidden_links_dict
        if bibkg_id not in writed_links_dict:
            writed_links_dict[bibkg_id] = wikidata_id    
            self.count_links += 1
            self.count_journal_links += 1
            dblp_id = self.dblp_ids_dict.get(bibkg_id)
            if not dblp_id:
                dblp_id = ''
            self.wikidata_linker.csv_data.setdefault(bibkg_id, [wikidata_id, dblp_id])
            self.wikidata_linker.csv_data[bibkg_id].append('linked_by_{}_recursion_journals'.format(self.link_type))
            #self.wikidata_linker.csv_data.append([bibkg_id, wikidata_id, 'linked_by_{}_recursion_journals'.format(self.link_type)])
        elif writed_links_dict[bibkg_id] != wikidata_id:
            if bibkg_id not in self.wikidata_linker.writed_id_entities:
                forbidden_links_dict[bibkg_id] = True
                del writed_links_dict[bibkg_id]
                self.count_fordidden_journal += 1
        else:
            self.wikidata_linker.csv_data[bibkg_id].append('linked_by_{}_recursion_journals'.format(self.link_type))    

    #link_by_parameters: enlaza BibKG con Wikidata enlazando entidades que forman parte de los valores de las propiedades de entidades
    #ya enlazadas entre BibKG con Wikidata
    #Se enlazan autores (link_authors()), publicaciones (link_publications()) y revistas (link_journals())
    def link_by_parameters(self, link_type):

        self.link_type = link_type
        print("Guardando datos de BibKG")
        #primer paso: guardar datos necesarios de BibKG en memoria
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

                if 'type' in entity:
                    type = entity['type']
                else:
                    type = 'unknown'
                
                #En caso de que la entidad posea un enlace con Wikidata
                wikidata_in_entity = 'wikidata' in entity
                if wikidata_in_entity or (id in self.wikidata_linker.writed_links_dict):
                    if wikidata_in_entity:
                        wikidata_id = entity['wikidata']    
                    else:
                        wikidata_id = self.wikidata_linker.writed_links_dict[id]

                    #link_publications
                    if type == 'Person':
                        name = process_names(entity['name'])
                        self.bibkg_author_dict[id] = {'id':id, 'name':name, 'publications':{}}
                        self.author_wikidata_id_dict[wikidata_id] = self.bibkg_author_dict[id]
                    
                    #link_authors
                    elif 'has_author' in entity:
                        if 'name' in entity:
                            name = entity['name']
                        else:
                            name = process_author_id(id)
                        name = process_names(name)

                        authors_dict = {}
                        for author in entity['has_author']:
                            author_id = author['value']
                            authors_dict[author_id] = {'id':author_id}
                            if 'orden' in author:
                                authors_dict[author_id]['orden'] = author['orden']

                        self.bibkg_publications_dict[wikidata_id] = {'id':id, 'name':name, 'has_author':authors_dict}
                        
                    #link journals
                    if 'in_journal' in entity:
                        entity_journal = entity['in_journal']
                        if wikidata_id in self.bibkg_publications_dict:
                            self.bibkg_publications_dict[wikidata_id]['in_journal'] = entity_journal
                        else:
                            self.bibkg_publications_dict[wikidata_id] = {'id':id, 'in_journal':entity_journal}



        print("Agregando IDs a propiedades que asocian entidades")
        for key, entity in self.bibkg_publications_dict.items():
            id = entity['id']
            if 'has_author' in entity:
                for author_id, author in entity['has_author'].items():
                    #author_id = author['id']

                    if author_id in self.bibkg_author_dict:
                        author['name'] = self.bibkg_author_dict[author_id]['name']
                        self.bibkg_author_dict[author_id]['publications'][id] = entity


        print("Leyendo personas de Wikidata")

        with open(self.wikidata_linker.wikidata_person_path, 'r') as wikidata_person:
            for linea in wikidata_person:
                entity = json.loads(linea)
                id = entity['id']
                self.wikidata_person_dict[id] = {'publications':{}}
                if 'en' in entity['name']:
                    self.wikidata_person_dict[id]['name'] = entity['name']['en']['value']
                else:
                    for _, valor in entity['name'].items():
                        self.wikidata_person_dict[id]['name'] = valor['value']
                        break
                
        print("Leyendo publicaciones de Wikidata")

        with open(self.wikidata_linker.wikidata_scholar_path, 'r') as wikidata_scholar:
            for linea in wikidata_scholar:
                entity = json.loads(linea)
                wikidata_id = entity['id']
                claims = entity['claims']

                #Analizar caso de autores en publicaciones (link_authors)
                if wikidata_id in self.bibkg_publications_dict:
                    bibkg_entity = self.bibkg_publications_dict[wikidata_id]
                    claims = entity['claims']

                    #Incorporar author strings de Wikidata
                    # if self.wikidata_author_string_property in claims:
                    #     authors = claims[self.wikidata_author_string_property]
                    #     for author in authors:
                    #         if 'datavalue' in author['mainsnak']:
                    #             #try:
                    #             wikidata_author_id = author['mainsnak']['datavalue']['value']
                    #             self.string_authors_dict[wikidata_author_id] = wikidata_author_id

                    #Caso de entidades de autores de publicaciones
                    if self.wikidata_author_property in claims and 'has_author' in bibkg_entity:
                        authors = claims[self.wikidata_author_property]
                        author_names_list_bibkg = {}
                        order_list_bibkg = {}
                        for _, value in bibkg_entity['has_author'].items():
                            if 'name' in value:
                                #Procesar nombre de BibKG
                                bibkg_person_id = value['id']
                                #except:
                                #print(value)
                                bibkg_person_name = value['name']
                                # print(bibkg_person_name)
                                # print(bibkg_person_id)
                                processed_name = process_names(bibkg_person_name)
                                author_names_list_bibkg[processed_name] = bibkg_person_id
                                if 'orden' in value:
                                    order_list_bibkg[value['orden']] = processed_name

                        for author in authors:
                            if 'datavalue' in author['mainsnak']:
                                wikidata_author_id = author['mainsnak']['datavalue']['value']
                                try:
                                    wikidata_author_name = self.wikidata_person_dict[wikidata_author_id]['name']
                                except:
                                    wikidata_author_name = None
                                if 'order' in author:
                                    wikidata_author_order = author['order']
                                    name_order = order_list_bibkg.get(wikidata_author_order)
                                    bibkg_id = ''
                                    if name_order:
                                        bibkg_id = author_names_list_bibkg.get(name_order)
                                        #bibkg_id = author_names_list_bibkg[name_order]
                                    else:
                                        if wikidata_author_name:
                                            wikidata_author_name = process_names(wikidata_author_name)
                                            bibkg_id = author_names_list_bibkg.get(wikidata_author_name)
                                        #bibkg_id = author_names_list_bibkg[wikidata_author_name]
                                    if bibkg_id:
                                        self.link_authors(bibkg_id, wikidata_author_id)
                                else:
                                    if wikidata_author_name:
                                        wikidata_author_name = process_names(wikidata_author_name)
                                        bibkg_id = author_names_list_bibkg.get(wikidata_author_name)
                                        if bibkg_id:
                                            self.link_authors(bibkg_id, wikidata_author_id)
                
                #Almacenar publicaciones de autores para link_publications
                if self.wikidata_author_property in claims:
                    authors = claims[self.wikidata_author_property]
                    for author in authors:
                        if 'datavalue' in author['mainsnak']:
                            wikidata_author_id = author['mainsnak']['datavalue']['value']
                            if wikidata_author_id in self.author_wikidata_id_dict:
                                author_entity = {}
                                if 'name' in entity:
                                    if len(entity['name']) > 0:
                                        #Tomar el primer nombre disponible de la entidad (para casos con múltiples idiomas en el nombre)
                                        author_entity['name'] = process_names(entity['name'][next(iter(entity['name']))]['value'])
                                    #tomar distintos aliases
                                    if 'aliases' in entity:
                                        author_entity['aliases'] = []
                                        for key, alias in entity['aliases'].items():
                                            for subalias in alias:
                                                alias_value = subalias['value']
                                                author_entity['aliases'].append(process_names(alias_value))

                                if wikidata_author_id in self.wikidata_person_dict:
                                    self.wikidata_person_dict[wikidata_author_id]['publications'][wikidata_id] = author_entity

                #Para caso link_journals
                if self.wikidata_published_in_property in claims:
                    bibkg_entity = self.bibkg_publications_dict.get(wikidata_id)
                    if bibkg_entity and 'in_journal' in bibkg_entity:
                        bibkg_journal_id = bibkg_entity['in_journal'][0]['value']
                        #print(bibkg_journal_id)
                        publishers = claims[self.wikidata_published_in_property]
                        n_publishers = len(publishers)
                        if n_publishers == 1:
                            for publisher in publishers:
                                if 'datavalue' in publisher['mainsnak']:
                                    wikidata_journal_id = publisher['mainsnak']['datavalue']['value']
                                    self.link_journals(bibkg_journal_id, wikidata_journal_id)

        
        print("Comparando publicaciones de autores")
        #Comparar publicaciones de autores de Wikidata con BibKG guardados en memoria
        for key, wikidata_entity in self.wikidata_person_dict.items():
            wikidata_publications = wikidata_entity['publications']
            if key in self.author_wikidata_id_dict:
                bibkg_entity = self.author_wikidata_id_dict[key] #####
                bibkg_publications = bibkg_entity.get('publications')

                if bibkg_publications:
                
                    name_values = [publication['name'] for publication in bibkg_publications.values() if 'name' in publication]
                    repeated_names = set()
                    for name in name_values:
                        if name_values.count(name) > 1:
                            repeated_names.add(name)
                    for bibkg_key, bibkg_publication in bibkg_publications.items():
                        if 'name' in bibkg_publication:
                            bibkg_name = bibkg_publication['name']

                            # definir parametros de comparacion
                            for wikidata_key, value in wikidata_publications.items():
                                if 'name' in value and bibkg_name not in repeated_names:
                                    wikidata_name = value['name']
                                    if bibkg_name == wikidata_name:
                                        self.count_publication_relations += 1
                                        self.link_publications(bibkg_key, wikidata_key)
                                    elif 'aliases' in bibkg_publication:
                                        bibkg_aliases = bibkg_publication['aliases']
                                        if wikidata_name in bibkg_aliases:
                                            self.count_publication_relations += 1
                                            self.link_publications(bibkg_key, wikidata_key)

        print(self.count_links)
        print(self.count_author_links)
        print(self.count_publication_links)
        print(self.count_journal_links)

        print(self.count_fordidden_author)
        print(self.count_fordidden_publication)
        print(self.count_fordidden_journal)

        print(self.count_publication_relations)            
        return self.count_links



