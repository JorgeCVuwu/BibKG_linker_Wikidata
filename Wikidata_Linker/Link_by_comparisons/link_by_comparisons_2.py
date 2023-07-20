import json
import re
import time
import os
import csv
from unidecode import unidecode

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
    if not name:
        return False
    name = str(name)
    split = name.split()
    resultado = name.replace(".", "").lower()
    if len(split) == 3:
        if (len(split[1]) == 2 and "." in split[1]) or len(split[1]) == 1:
            resultado = split[0] + ' ' + split[2]
        elif is_number(split[2]):
            resultado = split[0] + ' ' + split[1]
        # else:
        #     print(name)
    return unidecode(resultado)

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

class LinkByComparisons():

    def __init__(self, wikidata_linker):
        self.wikidata_linker = wikidata_linker

        self.dblp_ids_dict = {}
        
        self.bibkg_person_dict = {}
        self.property_dict_name = {}
        self.wikidata_person = {}

        self.count_links = 0

    #add_property: crea diccionarios de almacenamiento de datos para cada tipo de parámetro de comparación, según el nombre de la propiedad
    #El diccionario posee como llave el string de los nombres, que posee asociado un set() de IDs con ese nombre
    def add_property(self, entity, property):

        id = entity['id']
        property_dict_name = property + '_dict'
        #se crea el diccionario y se añade al objeto como atributo de no existir previamente
        if not hasattr(self, property_dict_name):
            setattr(self, property_dict_name, {})
        if property in entity:
            property_value = entity[property]
            if property == 'name':
                property_value = process_names(property_value)
            property_dict = getattr(self, property_dict_name)
            property_dict.setdefault(property_value, set())
            property_dict[property_value].add(id)

    #add_name: almacena el atributo name de BibKG en memoria
    def add_name(self, entity):
        self.add_property(entity, "name")
    
    #add_authors: añade a un diccionario de LinkByComparisons la entidad asociada al conjunto de autores de una entidad con un formato especifico
    #formato: author1_1##author2_2##author3_3
    # '##' separa a autores, y '_n' es el orden asociado a cada autor, siendo 'n' el valor del orden 
    def add_authors(self, entity):

        id = entity['id']
        property_dict_name = 'author_dict'
        if not hasattr(self, property_dict_name):
            setattr(self, property_dict_name, {})
        if 'has_author' in entity:
            author_dict = self.author_dict
            author_key = ''
            first_author = True
            for author in entity['has_author']:
                if not first_author:
                    author_key += '##'
                first_author = False
                author_value = author['value']
                if author_value in self.bibkg_person_dict:
                    author_key += process_names(self.bibkg_person_dict[author_value])
                else:
                    author_key += process_names(process_author_id(author_value))
                if 'orden' in author:
                    orden = author['orden']
                    author_key += '_' + str(orden)
            if author_key not in author_dict:
                author_dict[author_key] = set()
            author_dict[author_key].add(id)

    #add_date: almacena el atributo year de BibKG en memoria
    def add_date(self, entity):
        self.add_property(entity, "year")

    #add_url: almacena el atributo url de BibKG en memoria
    def add_url(self, entity):
        self.add_property(entity, 'url')

    #compare_name: retorna una lista con todas las entidades de BibKG que poseen el mismo nombre que la entidad de Wikidata analizada
    def compare_name(self, entity):
        return_id_list = set()
        wikidata_names = entity['name']
        for _, name_value in wikidata_names.items():
            processed_name = process_names(name_value['value'])
            if processed_name in self.name_dict:
                id_list = self.name_dict[processed_name]
                return_id_list.update(id_list)
        return return_id_list

    #compare_aliases: retorna una lista con todas las entidades de BibKG que poseen el mismo nombre que alguno de los aliases de la 
    #entidad de Wikidata
    def compare_aliases(self, entity):
        return_id_list = set()
        if 'aliases' in entity:
            aliases = entity['aliases']
            for _, value in aliases.items():
                for alias_list in value:
                    alias_value = process_names(alias_list['value'])
                    try:
                        id_list = self.name_dict[alias_value]
                        return_id_list.update(id_list)
                    except:
                        pass
        return return_id_list

    #compare_authors: verifica si dos entidades de BibKG y Wikidata poseen los mismos autores en común (junto con el mismo orden entre ellos)
    def compare_authors(self, entity, bibkg_id):

        property = 'P50'
        author_string_property = 'P2093'
        claims = entity['claims']
        authors = ''
        authors_entities_dict = {}
        authors_string_dict = {}
        if property in claims:
            authors_dict = claims[property]
            for author_object in authors_dict:
                if 'datavalue' in author_object['mainsnak']:
                    author_id = author_object['mainsnak']['datavalue']['value']
                    author_name = self.wikidata_person.get(author_id)
                    if author_name:    
                        author_value = process_names(author_name)
                        if 'order' in author_object: 
                            author_order = author_object['order']
                            authors_entities_dict[author_order] = author_value

        if author_string_property in claims:
            authors_dict = claims[author_string_property]
            for author_object in authors_dict:
                if 'datavalue' in author_object['mainsnak']:
                    author_value = process_names(author_object['mainsnak']['datavalue']['value'])
                    if 'order' in author_object:            
                        author_order = author_object['order']
                        authors_string_dict[author_order] = author_value

        #Se añaden las entidades de la propiedad string dict a las de la propiedad author, si es que no existe ya un orden similar.
        authors_entities_dict.update(authors_string_dict)
        #se ordenan las entidades según su orden de autor
        authors_entities_dict = sorted(authors_entities_dict.items())
        #se crea el string con el mismo formato de add_authors()
        for order, value in authors_entities_dict:
            if authors:
                authors += '##'
            authors += value + '_' + order
        
        if authors in self.author_dict:
            authors_id = self.author_dict[authors]
            if bibkg_id in authors_id:
                #count += 1
                return True
            else:
                return False

    #compare_date: verifica si dos entidades de BibKG y Wikidata poseen el mismo año como fecha asociada al objeto (de existir entre ambos)
    #si no existe fecha en alguno de estos, se arroja True por defecto
    def compare_date(self, entity, bibkg_id):

        date_property = 'P577'

        if date_property in entity['claims'] and 'datavalue' in entity['claims'][date_property][0]['mainsnak']:
            date_value = entity['claims'][date_property][0]['mainsnak']['datavalue']['value']['time']
            processed_year = get_year(date_value)

            if processed_year in self.year_dict:
                id_list = self.year_dict[processed_year]
                if bibkg_id in id_list:
                    #count += 1
                    return True
                else:
                    return False
        #Analizar esto
        return True   
            
    #compare_url: compara los URLs asociados entre las entidades de BibKG y Wikidata, retorna la lista de IDs con el URL asociado
    def compare_url(self, entity):
        return_id_list = set()
        official_website = 'P856'
        full_work_at_url = 'P953'
        if full_work_at_url in entity:
            property_value = entity[full_work_at_url]
            if property_value in self.url_dict:
                return_id_list.update(self.url_dict[property_value])
        if official_website in entity:
            property_value = entity[official_website]
            if property_value in self.url_dict:
                return_id_list.update(self.url_dict[property_value])
        return return_id_list

    #link_authors: si se cumplen las condiciones, enlaza entidades  de BibKG y Wikidata
    def link_entities(self, bibkg_id, wikidata_id):
        writed_links_dict = self.wikidata_linker.writed_links_dict
        forbidden_links_dict = self.wikidata_linker.forbidden_links_dict
        if bibkg_id not in writed_links_dict:
            if bibkg_id not in forbidden_links_dict:
                #self.wikidata_linker.csv_data.append([bibkg_id, wikidata_id, 'linked_by_comparisons'])
                dblp_id = self.dblp_ids_dict.get(bibkg_id)
                if not dblp_id:
                    dblp_id = ''
                bibkg_id_link = self.wikidata_linker.writed_wikidata_id_entities.get(wikidata_id)
                if ((bibkg_id_link and bibkg_id_link == bibkg_id) or not bibkg_id_link):
                    writed_links_dict[bibkg_id] = wikidata_id
                    self.count_links += 1
                    self.wikidata_linker.csv_data.setdefault(bibkg_id, [wikidata_id, dblp_id])
                    self.wikidata_linker.csv_data[bibkg_id].append('linked_by_comparisons')
        #Si una entidad es relacionada con otra entidad a la ya asociada, se elimina la asociación
        elif writed_links_dict[bibkg_id] != wikidata_id:
            if bibkg_id not in self.wikidata_linker.writed_id_entities:
                forbidden_links_dict[bibkg_id] = True
                del writed_links_dict[bibkg_id]
        else:
            self.wikidata_linker.csv_data[bibkg_id].append('linked_by_comparisons')    

    #link_by_comparisons: realiza el método de enlaces por comparaciones, enlazando entidades de BibKG con Wikidata mediante coincidencias
    #en las propiedades de estas
    #Utiliza ciertas propiedades como potenciales entidades a enlazar (nombres, aliases) y otros para validar la comparación (año, autores)
    #Debe existir exactamente 1 entidad de BibKG que cumpla las condiciones con la de Wikidata para realizar el enlazamiento.
    def link_by_comparisons(self):

        bibkg_path = self.wikidata_linker.bibkg_path
        
        #Almacenar entidades de personas de BibKG
        with open(bibkg_path, 'r') as bibkg:
            for linea in bibkg:
                entity = json.loads(linea)
                id = entity['id']

                if 'key' in entity:
                    self.dblp_ids_dict[id] = entity['key']
                elif ':url' in entity:
                    dblp_id = get_dblp_url(entity)
                    if dblp_id:
                        self.dblp_ids_dict[id] = dblp_id


                if 'type' in entity:
                    type = entity['type']
                    if type == "Person":
                        self.bibkg_person_dict[id] = entity['name']

        
        print("Almacenando entidades de BibKG")

        #lista de funciones de almacenamiento en memoria de BibKG (acá se pueden añadir nuevas funciones)
        add_functions_list = [self.add_name, self.add_authors, self.add_date, self.add_url]
        with open(bibkg_path, 'r') as bibkg:
            for linea in bibkg:
                entity = json.loads(linea)
                id = entity['id']
                for add_function in add_functions_list:
                    add_function(entity)
                #bibkg_entity_dict[id] = entity_dict

        print("Almacenando nombres de personas de Wikidata")

        wikidata_person_dict = self.wikidata_person

        with open(self.wikidata_linker.wikidata_person_path, 'r') as wikidata_person:
            for linea in wikidata_person:
                entity = json.loads(linea)
                id = entity['id']
                if 'name' in entity:
                    try:
                        wikidata_person_dict[id] = next(iter(entity['name'].items()))[1]['value']
                    except:
                        pass



        print("Comparando con entidades de Wikidata")
        with open(self.wikidata_linker.wikidata_scholar_path, 'r') as wikidata_scholar:
            for linea in wikidata_scholar:
                entity = json.loads(linea)
                id = entity['id']
                names_id_list = self.compare_name(entity)
                aliases_id_list = self.compare_aliases(entity)
                url_id_list = self.compare_url(entity)
                names_id_list.update(aliases_id_list)
                names_id_list.update(url_id_list)

                #Lista con las funciones de comparación para descartar entidades con valores distintos en una misma propiedad
                compare_functions_list = [self.compare_date, self.compare_authors]
                total_entities = []
                if len(names_id_list) > 0:
                    for name_id in names_id_list:
                        parameters_boolean = True
                        for compare_function in compare_functions_list:
                            if not compare_function(entity, name_id):
                                parameters_boolean = False
                                break
                        if parameters_boolean:
                            total_entities.append(name_id)
                n_total_entities = len(total_entities)

                if n_total_entities == 1:
                    self.link_entities(total_entities[0], id)
                    #self.wikidata_linker.writed_links_dict[total_entities[0]] = id

        return self.count_links
