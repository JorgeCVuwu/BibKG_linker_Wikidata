import csv
import json
import os

class WikidataLinkerTester():
    

    def __init__(self) -> None:
        folder = 'data/wikidata_linker/'
        self.id_linked_entities_path = folder + 'id-links-4.csv'
        self.linked_entities_path = folder + 'linked-entities-3.csv'
        self.bibkg_path = 'db/JSON/bibkg.json'
        carpeta_externa = "D:\Memoria" 
        wikidata_person_name = "wikidata_person_4.json"
        wikidata_scholar_name = "wikidata_scholar_4.json"

        self.wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
        self.wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

        self.bibkg_id_links = {}
        self.wikidata_id_links = {}
        
        self.count_wikidata_previously_linked = 0
        self.count_wikidata_previously_linked_in_csv = 0

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
                bibkg_id = entity['id']

                #Datos respecto a las entidades previamente enlazadas en Wikidata
                wikidata_previously_linked_id = entity.get('wikidata')
                if wikidata_previously_linked_id: 
                    if bibkg_id in self.bibkg_id_links:
                        self.count_wikidata_previously_linked_in_csv += 1
                    self.count_wikidata_previously_linked += 1


    def charge_wikidata_test_data(self):
        print("Cargando JSON de personas de Wikidata")
        with open(self.wikidata_person_path, 'r') as wikidata_person:
            for linea in wikidata_person:
                entity = json.loads(linea)

        print("Cargando JSON de publicaciones de Wikidata")
        with open(self.wikidata_scholar_path, 'r') as wikidata_scholar:
            for linea in wikidata_scholar:
                entity = json.loads(linea)

    def charge_test_data(self):
        self.charge_csv_test_data()
        self.charge_bibkg_test_data()
        self.charge_wikidata_test_data()        


    def test_previously_linked_entities(self):
        print("Entidades de BibKG enlazadas previamente con Wikidata: {}".format(self.count_wikidata_previously_linked))
        print("Entidades de BibKG enlazadas previamente con Wikidata y en los CSV: {}".format(self.count_wikidata_previously_linked_in_csv))

    

if __name__ == "__main__":

    tester = WikidataLinkerTester()

    tester.charge_test_data()

    tester.test_previously_linked_entities()