import os
import csv
import time
from Link_by_id import link_by_id
from Link_by_parameters import link_journals, link_authors, link_publications
from Link_by_comparisons import link_by_comparisons

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

        self.time = 0

    #set_csv_data: inserta los parametros a insertar en el archivo CSV de los datos principales
    def set_csv_data(self, parameters_list):
        self.csv_data = [
            [parameters_list]
            #['entity_id', 'wikidata_id', 'link_method']
        ]

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



    def link_by_parameters(self):
        pass
        #link_by_parameters.link_by_parameters(self)

    def link_by_comparisons(self):
        pass
        #link_by_comparisons.link_by_comparisons(self)

    
if __name__ == "__main__":

    json_folder = "db/JSON/"
    bibkg_path = json_folder + "bibkg.json"

    carpeta_externa = "D:\Memoria" 
    wikidata_person_name = "wikidata_person_4.json"
    wikidata_scholar_name = "wikidata_scholar_4.json"

    wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
    wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

    wikidata_linker = WikidataLinker(bibkg_path, wikidata_person_path, wikidata_scholar_path)

    #Flujo de enlazamiento

    wikidata_linker.link_by_id()

    while wikidata_linker.method_writed_links != 0:
        wikidata_linker.link_by_parameters()

    wikidata_linker.link_by_comparisons()

    while wikidata_linker.method_writed_links != 0:
        wikidata_linker.link_by_parameters()
    