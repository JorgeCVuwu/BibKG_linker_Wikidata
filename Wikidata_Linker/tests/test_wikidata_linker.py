import csv
import json
import re
import os
from unidecode import unidecode
from statistics import mean

def is_number(string):
    patron = r'^\d+$'
    if re.match(patron, string):
        return True
    else:
        return False

def process_names(name):
    if not name:
        return False
    name = str(name)
    split = name.split()
    resultado = name.replace(".", "").lower()
    if len(split) == 3:
        if (len(split[1]) == 2 and "." in split[1]) or len(split[1]) == 1:
            resultado = split[0] + ' ' + split[2]
        # elif is_number(split[2]):
        #     resultado = split[0] + ' ' + split[1]
        # else:
        #     print(name)
    return unidecode(resultado)

class WikidataLinkerTester():
    

    def __init__(self) -> None:

        #rutas
        folder = 'data/wikidata_linker/'
        self.id_linked_entities_path = folder + 'id-links-4.csv'
        self.linked_entities_path = folder + 'linked-entities-4.csv'
        self.bibkg_path = 'db/JSON/bibkg.json'
        carpeta_externa = "D:\Memoria" 
        wikidata_person_name = "wikidata_person_4.json"
        wikidata_scholar_name = "wikidata_scholar_4.json"
        self.wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
        self.wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)
        self.journals_json_path = folder + 'repeated_journal_links.json'

        self.bibkg_id_links = {}
        self.wikidata_id_links = {}

        self.bibkg_previous_id_links = {}
        self.wikidata_previous_id_links = {}
        
        #test_previously_linked_entities
        self.count_wikidata_previously_linked = 0
        self.count_wikidata_previously_linked_in_csv = 0
        self.count_wikidata_previously_error_links = 0
        self.count_previously_errors_link_type = {}
        self.id_linked_previously_errors = {}

        #test_dblp_properties_in_wikidata
        self.count_dblp_properties = 0
        self.count_linked_dblp_properties = 0
        self.count_dblp_authors = 0
        self.count_dblp_publications = 0
        self.count_linked_dblp_authors = 0
        self.count_linked_dblp_publications = 0

        #test_journal_json_data
        self.count_same_name_bibkg_journals = 0
        self.count_almost_same_name_bibkg_journals = 0
        self.count_total_wikidata_journals = 0
        self.count_same_name_journals = 0

        #test_linked_publication_authors y test_string_names
        self.string_authors_proportion_list = []
        self.linked_authors_proportion_list = []
        self.available_linked_authors_proportion_list = []

        self.total_string_authors_dict = {}
        self.total_author_entities_dict = {}
        

    def charge_csv_test_data(self):

        #Se guardan datos de todos los links
        print("Cargando CSV de enlaces totales")
        with open(self.linked_entities_path, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            first_line = True
            # Iterar sobre cada línea del archivo CSV
            for fila in lector_csv:

                if first_line:
                    self.linked_entities_header = fila
                    #print(fila) 
                    first_line = False
                
                else:
                    bibkg_id = fila[0]
                    wikidata_id = fila[1]

                    self.bibkg_id_links[bibkg_id] = {'bibkg-id':bibkg_id, 'wikidata-id':wikidata_id}

                    link_object = self.bibkg_id_links[bibkg_id]

                    self.wikidata_id_links[wikidata_id] = self.bibkg_id_links[bibkg_id]
                    for i in range(2, len(fila)):
                        csv_property = self.linked_entities_header[i]
                        property_value = fila[i]
                        if property_value:
                            link_object[csv_property] = property_value



        print("Cargando CSV de enlaces mediante IDs")
        with open(self.id_linked_entities_path, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            first_line = True        
            for fila in lector_csv:

                if first_line:
                    self.id_linked_entities_header = fila
                    #print(fila) 
                    first_line = False

                else:
                    bibkg_id = fila[0]
                    wikidata_id = fila[1]

                    link_object = self.bibkg_id_links[bibkg_id]
                    
                    for i in range(4, len(fila)):
                        csv_property = self.id_linked_entities_header[i]
                        property_value = fila[i]
                        if property_value:
                            link_object[csv_property] = property_value

        # for bibkg_id, objeto in self.bibkg_id_links.items():
        #     print(bibkg_id)
        #     print(objeto)
        #     break
                

                


    def charge_bibkg_test_data(self):

        print("Cargando JSON de BibKG")
        with open(self.bibkg_path, 'r') as bibkg:
            for linea in bibkg:
                entity = json.loads(linea)
                bibkg_name = entity.get('name')
                bibkg_id = entity['id']

                if bibkg_id in self.bibkg_id_links:
                    if bibkg_name:
                        self.bibkg_id_links[bibkg_id]['bibkg-name'] = process_names(bibkg_name)
                
                # one_cond = False
                # two_cond = False
                # if 'has_author' in entity:
                #     for author in entity['has_author']:
                #         if author['value'] == 'a_Benjamin_Poulter_0002' or author['value'] == 'a_Benjamin_Poulter_0001':
                #             if one_cond:
                #                 two_cond = True
                #                 break
                #             one_cond = True
                        
                # if two_cond:
                #     print(entity)
                #     break

                #Datos respecto a las entidades previamente enlazadas en Wikidata
                wikidata_previously_linked_id = entity.get('wikidata')
                if wikidata_previously_linked_id: 
                    if bibkg_id in self.bibkg_id_links:
                        self.count_wikidata_previously_linked_in_csv += 1
                        bibkg_csv = self.bibkg_id_links[bibkg_id]
                        bibkg_wikidata_id = bibkg_csv['wikidata-id']
                        if bibkg_wikidata_id != wikidata_previously_linked_id:
                            self.count_wikidata_previously_error_links += 1
                            for i in range(2, len(self.id_linked_entities_header)):
                                if self.id_linked_entities_header[i] in bibkg_csv:
                                    self.count_previously_errors_link_type[self.id_linked_entities_header[i]] = self.count_previously_errors_link_type.setdefault(self.id_linked_entities_header[i], 0) + 1
                                    
                                    self.id_linked_previously_errors.setdefault(bibkg_id,{'wikidata_previous_id':wikidata_previously_linked_id,'csv_wikidata_id':bibkg_wikidata_id})
                                    self.id_linked_previously_errors[bibkg_id][self.id_linked_entities_header[i]] = True
                    
                    else:
                        wikidata_id = wikidata_previously_linked_id
                        self.bibkg_previous_id_links[bibkg_id] = {'bibkg-id':bibkg_id, 'wikidata-id':wikidata_id}
                        self.wikidata_previous_id_links[wikidata_id] = self.bibkg_previous_id_links[bibkg_id]

                    self.count_wikidata_previously_linked += 1


    def charge_wikidata_test_data(self):
        # print("Cargando JSON de personas de Wikidata")
        # with open(self.wikidata_person_path, 'r') as wikidata_person:
        #     for linea in wikidata_person:
        #         entity = json.loads(linea)

        print("Cargando JSON de publicaciones de Wikidata")
        with open(self.wikidata_scholar_path, 'r') as wikidata_scholar:
            for linea in wikidata_scholar:
                entity = json.loads(linea)
                wikidata_id = entity['id']
                claims = entity['claims']

                wikidata_names = entity['name']
                if wikidata_id in self.wikidata_id_links:
                    self.wikidata_id_links[wikidata_id]['wikidata-name'] = wikidata_names

                
                #Propiedades de DBLP
                dblp_author_property = 'P2456'
                dblp_publication_property = 'P8978'
                dblp_venue_property = 'P8926'
                dblp_event_property = 'P10692'

                dblp_properties = [dblp_author_property, dblp_publication_property, dblp_venue_property, dblp_event_property]

                #Test: test_dblp_properties_in_wikidata()
                for property_id, content in claims.items():

                    if property_id in dblp_properties:
                        self.count_dblp_properties += 1

                        if property_id == dblp_author_property:
                            self.count_dblp_authors += 1
                        elif property_id == dblp_publication_property:
                            self.count_dblp_publications += 1

                        if wikidata_id in self.wikidata_id_links:
                            self.count_linked_dblp_properties += 1
                            if property_id == dblp_author_property:
                                self.count_linked_dblp_authors += 1
                            elif property_id == dblp_publication_property:
                                self.count_linked_dblp_publications += 1
                

                #test_linked_publication_authors y test_string_names
                if wikidata_id in self.wikidata_id_links:
                    for property_id, content in claims.items():
                        #author property
                        order_authors_dict = {}
                        count_linked_order_authors = 0
                        count_not_linked_order_authors = 0
                        count_string_order_authors = 0
                        if property_id == 'P50':
                            for author in claims[property_id]:
                                if 'datavalue' in author['mainsnak']:
                                    author_id = author['mainsnak']['datavalue'].get('value')
                                else:
                                    author_id = ''
                                if author_id and 'order' in author:
                                    wikidata_author_order = author['order']
                                    if author_id in self.wikidata_id_links or author_id in self.wikidata_previous_id_links:
                                        order_authors_dict[wikidata_author_order] = {'id':author_id, 'linked':True}
                                        count_linked_order_authors += 1
                                    else:
                                        order_authors_dict[wikidata_author_order] = {'id':author_id, 'linked':False}
                                        count_not_linked_order_authors += 1
                                    
                                    self.total_author_entities_dict[author_id] = self.total_author_entities_dict.setdefault(author_id, 0) + 1                           


                                                                                             

                        elif property_id == 'P2093':
                            for author in claims[property_id]:
                                if 'datavalue' in author['mainsnak']:
                                    author_name = author['mainsnak']['datavalue'].get('value')
                                else:
                                    author_name = ''
                                if author_name and 'order' in author:
                                    author_name = process_names(author_name)
                                    wikidata_author_order = author['order']
                                    if wikidata_author_order not in order_authors_dict:
                                        order_authors_dict[wikidata_author_order] = {'name':author_name}
                                        count_string_order_authors += 1

                                        self.total_string_authors_dict[author_name] = self.total_string_authors_dict.setdefault(author_name, 0) + 1
                        
                        count_total_order_authors = len(order_authors_dict)

                        linked_vs_total_proportion = count_linked_order_authors / count_total_order_authors
                        linked_vs_total_not_string_proportion = count_linked_order_authors / (count_linked_order_authors + count_not_linked_order_authors)
                        string_vs_total_proportion = count_string_order_authors / count_total_order_authors


                        self.linked_authors_proportion_list.append(linked_vs_total_proportion)
                        self.available_linked_authors_proportion_list.append(linked_vs_total_not_string_proportion)
                        self.string_authors_proportion_list.append(string_vs_total_proportion)
                        


                        #author string property
                        

                                    
                            

    def test_journal_json_data(self):
        print("Cargando JSON de journals enlazados de BibKG")
        with open(self.journals_json_path, 'r') as bibkg_journals:
            c_not_name = 0
            journal_entity = json.load(bibkg_journals)
            for wikidata_id, bibkg_id_list in journal_entity.items():
                len_bibkg_id_list = len(bibkg_id_list)
                wikidata_id_names = self.wikidata_id_links[wikidata_id].get('wikidata-name')
                bibkg_names_dict = {}
                for bibkg_id in bibkg_id_list:
                    bibkg_id_name = process_names(self.bibkg_id_links[bibkg_id]['bibkg-name'])
                    bibkg_names_dict[bibkg_id_name] = bibkg_names_dict.setdefault(bibkg_id_name, 0) + 1
                
                dominant_name = ''
                if len(bibkg_names_dict) == 1:
                    self.count_same_name_bibkg_journals += 1
                    dominant_name = list(bibkg_names_dict)[0]
                if len(bibkg_names_dict) / len_bibkg_id_list > 0.8:
                    self.count_almost_same_name_bibkg_journals += 1
                    dominant_name = max(bibkg_names_dict, key=lambda clave: bibkg_names_dict[clave])
                self.count_total_wikidata_journals += 1

                if dominant_name and wikidata_id_names:
                    for name_value in wikidata_id_names.values():
                        processed_name = process_names(name_value['value'])
                        if processed_name == dominant_name:
                            self.count_same_name_journals += 1
                            break
                elif not wikidata_id_names:
                    c_not_name += 1
        print(c_not_name)
            
        print("Total de entidades de journals de Wikidata enlazadas: {}".format(self.count_total_wikidata_journals))
        print("Total de entidades de Wikidata con journals de BibKG con el mismo nombre: {}".format(self.count_same_name_bibkg_journals))
        print("Total de entidades de Wikidata con al menos 80/100 de journals de BibKG con el mismo nombre: {}".format(self.count_almost_same_name_bibkg_journals))
        print("Total de entidades de journals de Wikidata enlazadas con entidades de BibKG con el mismo nombre: {}".format(self.count_same_name_journals))



                
                    

    def charge_test_data(self):
        self.charge_csv_test_data()
        self.charge_bibkg_test_data()
        self.charge_wikidata_test_data()        

    #test_previously_linked_entities: printea los resultados relacionados con el enlazamiento con enlaces ya existentes en el JSON de BibKG
    def test_previously_linked_entities(self):
        print("Entidades de BibKG enlazadas previamente con Wikidata: {}".format(self.count_wikidata_previously_linked))
        print("Entidades de BibKG enlazadas previamente con Wikidata y en los CSV: {}".format(self.count_wikidata_previously_linked_in_csv))
        print("Entidades de BibKG que poseen un enlace de Wikidata previo y otro en el enlazamiento de datos: {}".format(self.count_wikidata_previously_error_links))
        print(self.count_previously_errors_link_type)

        # count_redirect = 0
        # for key, value in self.id_linked_previously_errors.items():
        #     previous_w_id = value['wikidata_previous_id']
        #     # if 'linked_by_id' in value:
        #     #     print(key)
        #     #     print(value)
        #     #     c+=1
        #     # if c > 15:
        #     #     break
        # print(count_redirect)

    def test_dblp_properties_in_wikidata(self):
        print("Total de entidades de Wikidata enlazados con DBLP: {}".format(self.count_dblp_properties))
        print("Total de entidades de Wikidata enlazados con DBLP y con BibKG: {}".format(self.count_linked_dblp_properties))

        print("Total de publicaciones de Wikidata enlazados con DBLP: {}".format(self.count_dblp_publications))
        print("Total de publicaciones de Wikidata enlazados con DBLP y con BibKG: {}".format(self.count_linked_dblp_publications))

        print("Total de autores de Wikidata enlazados con DBLP: {}".format(self.count_dblp_authors))
        print("Total de autores de Wikidata enlazados con DBLP y con BibKG: {}".format(self.count_linked_dblp_authors))

        linked_authors_percent = round((self.count_linked_dblp_authors/self.count_dblp_authors)*100, 2)
        linked_publications_percent = round((self.count_linked_dblp_publications/self.count_dblp_publications)*100, 2)
        linked_total_percent = round((self.count_linked_dblp_properties/self.count_dblp_properties)*100, 2)

        print("Porcentaje de autores enlazados: {}%".format(linked_authors_percent))
        print("Porcentaje de publicaciones enlazadas: {}%".format(linked_publications_percent))
        print("Porcentaje total de entidades enlazadas vs total en Wikidata: {}%".format(linked_total_percent))


    def test_linked_publication_authors(self):
        string_authors_proportion_mean = mean(self.string_authors_proportion_list)
        linked_authors_proportion_mean = mean(self.linked_authors_proportion_list)
        available_linked_authors_proportion_mean = mean(self.available_linked_authors_proportion_list)

        print("En los autores de publicaciones enlazadas con orden en los autores:")
        print("Promedio de proporción de strings de autores vs enlaces totales: {}".format(string_authors_proportion_mean))
        print("Promedio de proporción de autores enlazados vs enlaces totales: {}".format(linked_authors_proportion_mean))
        print("Promedio de proporción de autores enlazados vs autores con entidades en Wikidata: {}".format(available_linked_authors_proportion_mean))

    def test_string_authors(self):
        string_authors_len = len(self.total_string_authors_dict)
        entity_authors_len = len(self.total_author_entities_dict)

        string_authors_proportion = string_authors_len / (string_authors_len + entity_authors_len)
        print("En los autores de publicaciones enlazadas con orden en los autores:")
        print("Total de nombres procesados detectados en la propiedad string authors de publicaciones enlazadas: {}".format(string_authors_len))
        print("Total de entidades detectadas en la propiedad authors de publicaciones enlazadas: {}".format(entity_authors_len))
        print("Proporción de string authors respecto al total de autores detectados: {}".format(string_authors_proportion))

if __name__ == "__main__":

    tester = WikidataLinkerTester()

    #Cargar datos de testeo
    tester.charge_test_data()

    #Calcular y printear resultados
    tester.test_previously_linked_entities()    
    tester.test_dblp_properties_in_wikidata()
    tester.test_journal_json_data()
    tester.test_linked_publication_authors()
    tester.test_string_authors()