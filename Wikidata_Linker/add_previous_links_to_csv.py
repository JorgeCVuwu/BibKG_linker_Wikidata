import csv
import json

previous_bibkg_id_dict = {}
already_writed_previous_id_links = {}



archivo_json = 'db/json/bibkg_copy.json'
archivo_csv_1 = 'data/wikidata_linker/linked-entities-5-2.csv'

with open(archivo_json) as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'wikidata' in entity:
            previous_bibkg_id_dict[id] = entity['wikidata']
            
with open(archivo_csv_1, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    for fila in lector_csv:
        bibkg_id = fila[0]
        wikidata_id = fila[1]
        if bibkg_id in previous_bibkg_id_dict:
            already_writed_previous_id_links[bibkg_id] = True
    


count_new_links = 0


with open(archivo_csv_1, mode="a", newline="") as archivo:
    writer_csv = csv.writer(archivo)
    
    # Iterar sobre cada línea del archivo CSV
    for bibkg_id, wikidata_id in previous_bibkg_id_dict.items():
        if bibkg_id not in already_writed_previous_id_links:
            fila = [bibkg_id, wikidata_id, wikidata_id]
            for i in range(3, 13):
                fila.append('')
            writer_csv.writerow(fila)
            count_new_links += 1

print("Enlaces previos escritos: {}".format(count_new_links))

