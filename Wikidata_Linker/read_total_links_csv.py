import csv
import json

archivo_json = 'db/JSON/bibkg.json'
archivo_csv = 'data/wikidata_linker/linked-entities-3.csv'
count_linked_corr = 0

bibkg_id_dict = {}
wikidata_id_dict = {}

wikidata_repet_id_dict = {}

bibkg_repeats_in_wikidata = {}

count_wikidata_error_types = {}

count_bibkg_id_repetitions = 0
count_wikidata_id_repetitions = 0

count_hashtags = 0

count_only_comparisons = 0

with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:

        bibkg_id = fila[0]
        if bibkg_id[-4:-1] == '###':
            #print(bibkg_id)
            count_hashtags += 1
        wikidata_id = fila[1]
        bibkg_id_dict.setdefault(bibkg_id,[])
        bibkg_id_dict[bibkg_id].append(wikidata_id)
        wikidata_id_dict.setdefault(wikidata_id,[])
        wikidata_id_dict[wikidata_id].append(bibkg_id)
        if fila[7]:

            count_only_comparisons += 1
        if '_corr_' in bibkg_id:
            count_linked_corr += 1

count_repeated_bibkg_ids = 0
for key, value in bibkg_id_dict.items():
    if len(value) > 1:
        count_repeated_bibkg_ids += 1

count_repeated_wikidata_ids = 0
count_bibkg_with_repeated_wikidata = 0
max_entities_wikidata = 0
max_entities_wikidata_number = 0
for key, value in wikidata_id_dict.items():
    n = len(value)
    if n > 1:
        count_repeated_wikidata_ids += 1
        count_bibkg_with_repeated_wikidata += n
        if n > max_entities_wikidata_number:
            max_entities_wikidata_number = n
            max_entities_wikidata = key
    
    # if len(value) > 20:
    #     print(key)
    #     print(value)
    #     break

print(count_repeated_bibkg_ids)
print(count_repeated_wikidata_ids)
print(count_bibkg_with_repeated_wikidata)

print(max_entities_wikidata)
print(max_entities_wikidata_number)

        # if wikidata_id not in wikidata_id_dict:
        #     pass
            #wikidata_id_dict[wikidata_id] = bibkg_id
        # else:
        #     wikidata_repet_id_dict[bibkg_id] = wikidata_id
        #     if wikidata_id not in bibkg_repeats_in_wikidata:
        #         wikidata_repet_id_dict[wikidata_id_dict[wikidata_id]] = wikidata_id
        #         bibkg_repeats_in_wikidata[wikidata_id] = [wikidata_id_dict[wikidata_id]]
        #         count_wikidata_id_repetitions += 1
        #     bibkg_repeats_in_wikidata[wikidata_id].append(bibkg_id) 
        #     count_wikidata_id_repetitions += 1

# count_repeated_wikidata_ids = 0
# count_repeated_bibkg_entities = 0
# count_bibkg_entities = 0
# for key, value in wikidata_id_dict.items():
#     if len(value) > 1:
#         count_repeated_wikidata_ids += 1
#         count_repeated_bibkg_entities += len(value)
#     count_bibkg_entities += len(value)
#     # if count_repeated_wikidata_ids < 10:
#     #     print(key)
#     #     print(value)
#     #     print(len(value))

# print(count_hashtags)
# print(count_linked_corr)
# print(count_bibkg_entities)
# print(count_repeated_bibkg_entities)
# print(count_repeated_wikidata_ids)
# print(count_only_comparisons)


