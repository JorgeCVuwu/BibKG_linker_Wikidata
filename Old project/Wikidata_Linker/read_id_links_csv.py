import csv
import json

archivo_json = 'db/JSON/bibkg.json'
archivo_csv = 'data/wikidata_linker/id-links-5.csv'
archivo_csv_total = 'data/wikidata_linker/linked-entities-5.csv'
count_linked_corr = 0

bibkg_id_dict = {}
wikidata_id_dict = {}

checked_bibkg_id_dict = {}

count_wikidata_error_types = {}

count_bibkg_id_repetitions = 0
count_wikidata_id_repetitions = 0

count_previously_linked = 0
bibkg_previously_linked_dict = {}
count_writed_in_id_links = 0

count_hashtags = 0
count_other_wikidata_ids = 0

count_distinct_previously_linked = 0
count_fila_1_2 = 0

bibkg_previously_linked_in_total_dict = {}


with open(archivo_csv_total, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    first_line = True
    for fila in lector_csv:
        if first_line:
            first_line = False
            continue
        bibkg_id = fila[0]
        wikidata_id = fila[1]


        if fila[2]:
            count_previously_linked += 1
            bibkg_previously_linked_dict[bibkg_id] = wikidata_id

count_previous_in_id = 0
count_distinct_link = 0
with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    first_line = True
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:
        if first_line:
            first_line = False
            continue
        bibkg_id = fila[0]
        wikidata_id = fila[1]
        if bibkg_id in bibkg_previously_linked_dict:
            bibkg_previously_linked_in_total_dict[bibkg_id] = True
            if fila[1] != bibkg_previously_linked_dict[bibkg_id]:
                count_distinct_link += 1
                print(fila)
                break

print(count_distinct_link)
            
print(len(bibkg_previously_linked_in_total_dict))

id_link_type_dict = {}
id_link_first_type_dict = {}
id_link_type_previous_dict = {}
id_link_first_type_previous_dict = {}
with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    first_line = True
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:
        if first_line:
            csv_header = fila
            first_line = False
            continue
        bibkg_id = fila[0]
        if bibkg_id not in bibkg_previously_linked_in_total_dict:# and bibkg_id not in checked_bibkg_id_dict:
            for i in range(0, len(csv_header)):
                if fila[i]:
                    id_link_type_dict[csv_header[i]] = id_link_type_dict.setdefault(csv_header[i], 0) + 1
                    # if i == 2:
                    #     print(fila)
                    #     break  
            checked_bibkg_id_dict[bibkg_id] = True 
                
            for i in [len(csv_header) - 3, len(csv_header) - 1, len(csv_header) - 2]:# range(len(csv_header) - 3, len(csv_header)):
                if fila[i]:
                    id_link_first_type_dict[csv_header[i]] = id_link_first_type_dict.setdefault(csv_header[i], 0) + 1
                    break
        for i in range(0, len(csv_header)):
            if fila[i]:
                id_link_type_previous_dict[csv_header[i]] = id_link_type_previous_dict.setdefault(csv_header[i], 0) + 1
        for i in [len(csv_header) - 3, len(csv_header) - 1, len(csv_header) - 2]:
            if fila[i]:
                id_link_first_type_previous_dict[csv_header[i]] = id_link_first_type_previous_dict.setdefault(csv_header[i], 0) + 1
                break
        if fila[2]:
            count_other_wikidata_ids += 1
        wikidata_id = fila[1]
        bibkg_id_dict.setdefault(bibkg_id,[])
        bibkg_id_dict[bibkg_id].append(wikidata_id)
        wikidata_id_dict.setdefault(wikidata_id,[])
        wikidata_id_dict[wikidata_id].append(bibkg_id)
        if bibkg_id in bibkg_previously_linked_dict:
            count_writed_in_id_links += 1
            if wikidata_id != bibkg_previously_linked_dict[bibkg_id]:
                count_distinct_previously_linked += 1
            else:
                if fila[1] and fila[2]:
                    count_fila_1_2 += 1
        
        if '_corr_' in bibkg_id:
            count_linked_corr += 1
        else:
            count_bibkg_id_repetitions += 1



count_article_error = 0

count_repeated_bibkg_ids = 0

print(len(checked_bibkg_id_dict))

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

count_type_dict = {}
count_type_linked_dict = {}
count_type_linked_dict_2 = {}
count_already_linked = 0
count_already_linked_people = 0

print(id_link_type_dict)
print(id_link_type_previous_dict)
print(id_link_first_type_dict)
print(id_link_first_type_previous_dict)

print(len(repeated_bibkg_ids_dict))

