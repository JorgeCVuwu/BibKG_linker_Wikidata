import os
import csv
import time
from Link_by_id.link_by_id_2 import LinkByID
from Link_by_parameters import link_by_parameters
# from Link_by_comparisons import link_by_comparisons

#WikidataLinker: clase encargada de enlazar el JSON de BibKG con el archivo preprocesado de Wikidata
class WikidataLinker:

    def __init__(self, bibkg_path, wikidata_person_path, wikidata_scholar_path):
        #rutas de archivos
        self.bibkg_path = bibkg_path
        self.wikidata_person_path = wikidata_person_path
        self.wikidata_scholar_path = wikidata_scholar_path
        self.link_csv_path = "data/wikidata_linker/linked_entities.csv"
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

    #save_metadata_csv: guarda los metadatos del proceso (datos principales relacionados a la ejecución del proceso)
    def save_metadata_csv(self):
        with open(self.metadata_path, mode='w', newline='') as archivo_csv:             
            # Crea el objeto de escritura de CSV
            writer = csv.writer(archivo_csv)           
            # Escriba los datos en el archivo CSV
            data = [
                ['time_hours', 'writed_linked_entities'],
                [self.time, self.total_links_writed]
            ]
            for fila in data:
                writer.writerow(fila)

    #save_link_csv: crea el archivo CSV con todos los enlaces realizados, junto con las propiedades del proceso
    def save_link_csv(self):
        with open(self.link_csv_path, mode='w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            for fila in self.csv_data:
                writer.writerow(fila)

    
    def link_by_id(self):
        id_linker = LinkByID(self)
        id_linker.link_by_id()

    def link_by_parameters(self):
        id_linker = link_by_parameters.LinkByParameters()
        id_linker.link_by_parameters(self)

    def link_by_comparisons(self):
        pass
        #link_by_comparisons.link_by_comparisons(self)

    
if __name__ == "__main__":

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
        count_links = wikidata_linker.link_by_parameters()
        print(count_links)

    # wikidata_linker.link_by_comparisons()

    # while wikidata_linker.method_writed_links != 0:
    #     wikidata_linker.link_by_parameters()
    