import csv
import json

#json_file = 'db/JSON/bibkg.json'
archivo_csv = 'data/wikidata_linker/linked-entities.csv'
journals_json_path = 'data/wikidata_linker/repeated_journal_links.json'
count_linked_corr = 0

wikidata_id_dict = {}

with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:

        bibkg_id = fila[0]
        wikidata_id = fila[1]

        if (fila[6+1] or fila[10+1]) and bibkg_id != 'bibkg_id':
            wikidata_id_dict.setdefault(wikidata_id,[])
            wikidata_id_dict[wikidata_id].append(bibkg_id)

with open(journals_json_path, "w") as json_file:
    json.dump(wikidata_id_dict, json_file)

