import csv
import json

archivo_json = 'db/JSON/bibkg.json'
archivo_csv = 'data/wikidata_linker/id-links-3.csv'
count_linked_corr = 0

bibkg_id_dict = {}
wikidata_id_dict = {}

wikidata_repet_id_dict = {}

bibkg_repeats_in_wikidata = {}

count_wikidata_error_types = {}

count_bibkg_id_repetitions = 0
count_wikidata_id_repetitions = 0

count_hashtags = 0
count_other_wikidata_ids = 0

with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:
        bibkg_id = fila[0]
        if bibkg_id == 'a_Nicholas_J__Dobbins':
            print(fila)
        if fila[2]:
            count_other_wikidata_ids += 1
        if bibkg_id[-4:-1] == '###':
            #print(bibkg_id)
            count_hashtags += 1
        wikidata_id = fila[1]
        bibkg_id_dict.setdefault(bibkg_id,[])
        bibkg_id_dict[bibkg_id].append(wikidata_id)
        wikidata_id_dict.setdefault(wikidata_id,[])
        wikidata_id_dict[wikidata_id].append(bibkg_id)
        
        if '_corr_' in bibkg_id:
            count_linked_corr += 1
        else:
            count_bibkg_id_repetitions += 1



count_article_error = 0

count_repeated_bibkg_ids = 0

repeated_bibkg_ids_dict = {}
for key, value in bibkg_id_dict.items():
    if len(value) > 1:
        count_repeated_bibkg_ids += 1
        repeated_bibkg_ids_dict[key] = True
        # print(key)
        # print(value)
        # break

repeated_wikidata_ids_dict = {}
count_repeated_wikidata_ids = 0
for key, value in wikidata_id_dict.items():
    if len(value) > 1:
        count_repeated_wikidata_ids += 1
        repeated_wikidata_ids_dict[key] = True
        # print(key)
        # print("-")
        # print(value)
        # print("#############################")

count_repeated_bibkg_id_rows = 0
with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:
        bibkg_id = fila[0]
        wikidata_id = fila[1]
        if bibkg_id in repeated_bibkg_ids_dict:
            # if not fila[2]:
            #     print(fila)
            #     print("wjqefkehr")
            count_repeated_bibkg_id_rows += 1
        # if wikidata_id in repeated_wikidata_ids_dict and fila[1] == 'Q102442633':
        #     print(fila) 
        # else:
        #     if fila[2]:
        #         print(fila)

print(count_repeated_bibkg_ids)
print(count_repeated_wikidata_ids)

