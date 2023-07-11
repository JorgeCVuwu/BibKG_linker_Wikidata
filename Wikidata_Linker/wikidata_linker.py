import os
import csv
import time
from Link_by_id.link_by_id_2 import LinkByID
from Link_by_parameters import link_by_parameters
from Link_by_comparisons import link_by_comparisons_2
# from Link_by_comparisons import link_by_comparisons

#WikidataLinker: clase encargada de enlazar el JSON de BibKG con el archivo preprocesado de Wikidata
class WikidataLinker:

    def __init__(self, bibkg_path, wikidata_person_path, wikidata_scholar_path):
        #rutas de archivos
        self.bibkg_path = bibkg_path
        self.wikidata_person_path = wikidata_person_path
        self.wikidata_scholar_path = wikidata_scholar_path
        self.link_csv_path = "data/wikidata_linker/linked_entities.csv"
        self.link_id_csv_path = "data/wikidata_linker/linked_id_entities.csv"
        self.metadata_path = "data/wikidata_linker/metadata.csv"

        #contadores
        self.method_writed_links = -1

        self.total_links_writed = 0

        #Diccionarios que almacenan información referente a los enlaces
        self.writed_links_dict = {}
        self.forbidden_links_dict = {}

        self.csv_data = [
            ['entity_id', 'wikidata_id', 'link_method']
        ]

        self.time = 0

    #write_link_csv: crea el archivo CSV con todos los enlaces realizados, junto con las propiedades del proceso
    def write_links_csv(self):
        with open(self.link_csv_path, mode='w', newline='') as archivo_csv:
            self.count_link_types = {}
            writer = csv.writer(archivo_csv)
            for fila in self.csv_data:
                bibkg_id = fila[0]
                link_type = fila[2]
                if bibkg_id not in self.forbidden_links_dict:
                    writer.writerow(fila)
                    self.total_links_writed += 1
                    #se cuentan los tipos de enlaces en un diccionario según el tipo de enlace
                    self.count_link_types[link_type] = self.count_link_types.setdefault(link_type, 0) + 1
                    

        #write_metadata_csv: guarda los metadatos del proceso (datos principales relacionados a la ejecución del proceso y conteos de enlazamientos)
    def write_metadata_csv(self):
        with open(self.metadata_path, mode='w', newline='') as archivo_csv:             
            writer = csv.writer(archivo_csv)           
            data = [
                ['time_hours', 'writed_linked_entities'],
                [self.time, self.total_links_writed]
            ]
            for fila in data:
                writer.writerow(fila)

    def write_id_links_csv(self):
        with open(self.link_id_csv_path, mode='w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            for fila in self.csv_data:
                bibkg_id = fila[0]
                link_type = fila[2]
                if bibkg_id not in self.forbidden_links_dict:
                    writer.writerow(fila)





    #funciones link: enlazan entidades de BibKG con Wikidata (añadiéndolas a la lista que creará el CSV)
    
    #link_by_id: enlaza entidades mediante IDs (comparando las propiedades equivalentes que hacen referencia a IDs de distintas fuentes)
    def link_by_id(self):
        id_linker = LinkByID(self)
        id_linker.link_by_id()

    #link_by_parameters: enlaza entidades a partir de las entidades enlazadas desde el punto que se ejecuta la función,
    #a partir de las entidades a las que se hace referencia en las propiedades de las ya enlazadas
    def link_by_parameters(self):
        id_linker = link_by_parameters.LinkByParameters(self)
        return id_linker.link_by_parameters()

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

    count_links = 1

    while count_links != 0:
        count_links = wikidata_linker.link_by_parameters('id')
        print(count_links)

    count_links = 1

    count_links = wikidata_linker.link_by_comparisons()
    print(count_links)
    
    while count_links != 0:
        count_links = wikidata_linker.link_by_parameters('comparisons')
        print(count_links)

    fin = time.time()

    print("Tiempo de ejecución: {}".format(fin - inicio))

    # wikidata_linker.link_by_comparisons()

    # while wikidata_linker.method_writed_links != 0:
    #     wikidata_linker.link_by_parameters()
    