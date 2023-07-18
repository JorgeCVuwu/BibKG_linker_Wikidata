import os
import csv
import time
from Link_by_id.link_by_id_2 import LinkByID
from Link_by_parameters import link_by_parameters
from Link_by_comparisons import link_by_comparisons_2
# from Link_by_comparisons import link_by_comparisons

def get_strings_with_prefix(lista, prefix):
    prefix_values = [value.replace(prefix, '') for value in lista if value.startswith(prefix)]
    return prefix_values

#WikidataLinker: clase encargada de enlazar el JSON de BibKG con el archivo preprocesado de Wikidata
class WikidataLinker:

    def __init__(self, bibkg_path, wikidata_person_path, wikidata_scholar_path):
        #rutas de archivos
        self.bibkg_path = bibkg_path
        self.wikidata_person_path = wikidata_person_path
        self.wikidata_scholar_path = wikidata_scholar_path
        self.link_csv_path = "data/wikidata_linker/linked-entities-3.csv"
        self.link_id_csv_path = "data/wikidata_linker/linked-id-entities-3.csv"
        self.metadata_path = "data/wikidata_linker/metadata-3.csv"

        #contadores

        self.total_links_writed = 0
        self.count_forbidden = 0

        #Diccionarios que almacenan información referente a los enlaces
        self.writed_links_dict = {}
        self.forbidden_links_dict = {}
        self.writed_id_entities = {}

        self.csv_data_header = [
            'bibkg_id', 'wikidata_id', 'other_wikidata_ids', 'dblp_id', 'linked_by_id', 'linked_by_id_recursion_authors', 
            'linked_by_id_recursion_journals', 'linked_by_id_recursion_publications', 'linked_by_comparisons', 
            'linked_by_comparisons_recursion_authors',  'linked_by_comparisons_recursion_journals', 
            'linked_by_comparisons_recursion_publications'
        ]

        self.csv_data = {}

        self.time = 0

    #write_link_csv: crea el archivo CSV con todos los enlaces realizados, junto con las propiedades del proceso
    def write_links_csv(self):
        with open(self.link_csv_path, mode='w', newline='') as archivo_csv:
            self.count_link_types = {}
            writer = csv.writer(archivo_csv)
            writer.writerow(self.csv_data_header)
            try:
                for bibkg_id, link_data in self.csv_data.items():
                    wikidata_id = link_data[0]
                    dblp_id = link_data[1]
                    repeated_wikidata_ids = get_strings_with_prefix(link_data, 'wid###')
                    repeated_wikidata_ids_string = ''
                    for repeated_id in repeated_wikidata_ids:
                        if repeated_wikidata_ids_string:
                            repeated_wikidata_ids_string += '###'
                        repeated_wikidata_ids_string += repeated_id
                    fila = [bibkg_id, wikidata_id,repeated_wikidata_ids_string, dblp_id] # añadir DBLP ID, de existir
                    for link_properties in self.csv_data_header[4:]:
                        if link_properties in link_data:
                            fila.append('1')
                        else:
                            fila.append('')

                    if bibkg_id not in self.forbidden_links_dict:
                        writer.writerow(fila)
                        self.total_links_writed += 1
                    else:
                        self.count_forbidden += 1
                        #se cuentan los tipos de enlaces en un diccionario según el tipo de enlace
            except ValueError as e:
                print(e)
                print(bibkg_id)
                print(link_data)
                                                    

        #write_metadata_csv: guarda los metadatos del proceso (datos principales relacionados a la ejecución del proceso y conteos de enlazamientos)
    def write_metadata_csv(self):
        with open(self.metadata_path, mode='w', newline='') as archivo_csv:             
            writer = csv.writer(archivo_csv)           
            data = [
                ['time_hours', 'writed_linked_entities'],
                [self.time/3600, self.total_links_writed]
            ]
            for fila in data:
                writer.writerow(fila)

    # def write_id_links_csv(self):
    #     with open(self.link_id_csv_path, mode='w', newline='') as archivo_csv:
    #         writer = csv.writer(archivo_csv)
    #         for fila in self.csv_data:
    #             bibkg_id = fila[0]
    #             link_type = fila[2]
    #             if bibkg_id not in self.forbidden_links_dict:
    #                 writer.writerow(fila)





    #funciones link: enlazan entidades de BibKG con Wikidata (añadiéndolas a la lista que creará el CSV)
    
    #link_by_id: enlaza entidades mediante IDs (comparando las propiedades equivalentes que hacen referencia a IDs de distintas fuentes)
    def link_by_id(self):
        id_linker = LinkByID(self)
        id_linker.link_by_id()

    #link_by_parameters: enlaza entidades a partir de las entidades enlazadas desde el punto que se ejecuta la función,
    #a partir de las entidades a las que se hace referencia en las propiedades de las ya enlazadas
    def link_by_parameters(self, link_type):
        id_linker = link_by_parameters.LinkByParameters(self)
        return id_linker.link_by_parameters(link_type)

    #link_by_comparisons: enlaza entidades mediante comparación de propiedades con el mismo valor (descartando o asegurando enlaces)
    #no se consideran a las propiedades de IDs en este paso (se consideraron en link_by_id)
    def link_by_comparisons(self):
        id_linker = link_by_comparisons_2.LinkByComparisons(self)
        return id_linker.link_by_comparisons()
        #link_by_comparisons.link_by_comparisons(self)


    
if __name__ == "__main__":

    inicio = time.time()

    json_folder = "db/JSON/"
    bibkg_path = json_folder + "bibkg.json"

    #Rutas de los archivos del proceso
    carpeta_externa = "D:\Memoria" 
    wikidata_person_name = "wikidata_person_4.json"
    wikidata_scholar_name = "wikidata_scholar_4.json"

    wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
    wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

    wikidata_linker = WikidataLinker(bibkg_path, wikidata_person_path, wikidata_scholar_path)

    #Flujo de enlazamiento

    wikidata_linker.link_by_id()
    print(len(wikidata_linker.writed_links_dict))

    while True:
        count_links, count_articles, count_publications, count_journals = wikidata_linker.link_by_parameters('id')
        if count_articles == 0 or count_publications == 0:
            break

    count_links = wikidata_linker.link_by_comparisons()
    print(count_links)
    
    while True:
        count_links, count_articles, count_publications, count_journals = wikidata_linker.link_by_parameters('comparisons')
        if count_articles == 0 or count_publications == 0:
            break

    fin = time.time()

    wikidata_linker.time = fin - inicio

    wikidata_linker.write_links_csv()

    wikidata_linker.write_metadata_csv()

    print("Enlaces totales: {}".format(wikidata_linker.total_links_writed))

    print("Enlaces prohibidos: {}".format(wikidata_linker.count_forbidden))

    print("Tiempo de ejecución: {}".format(fin - inicio))

    