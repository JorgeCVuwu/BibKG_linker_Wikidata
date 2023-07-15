import csv
import json

archivo_json = 'db/JSON/bibkg.json'
archivo_csv = 'data/wikidata_linker/id-links-corr.csv'
count_linked_corr = 0

bibkg_id_dict = {}
wikidata_id_dict = {}

wikidata_repet_id_dict = {}

bibkg_repeats_in_wikidata = {}

count_wikidata_error_types = {}

count_bibkg_id_repetitions = 0
count_wikidata_id_repetitions = 0

count_hashtags = 0

with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:
        bibkg_id = fila[0]
        if bibkg_id[-4:-1] == '###':
            #print(bibkg_id)
            count_hashtags += 1
        wikidata_id = fila[1]
        if wikidata_id == 'Q33313196':
            print(bibkg_id)
            print(wikidata_id)
        if '_corr_' in bibkg_id:
            count_linked_corr += 1
        if bibkg_id not in bibkg_id_dict:
            bibkg_id_dict[bibkg_id] = True
        else:
            count_bibkg_id_repetitions += 1
        if wikidata_id not in wikidata_id_dict:
            wikidata_id_dict[wikidata_id] = bibkg_id
        else:
            wikidata_repet_id_dict[bibkg_id] = wikidata_id
            if wikidata_id not in bibkg_repeats_in_wikidata:
                wikidata_repet_id_dict[wikidata_id_dict[wikidata_id]] = wikidata_id
                bibkg_repeats_in_wikidata[wikidata_id] = [wikidata_id_dict[wikidata_id]]
                count_wikidata_id_repetitions += 1
            bibkg_repeats_in_wikidata[wikidata_id].append(bibkg_id) 
            count_wikidata_id_repetitions += 1

print(count_hashtags)
count_article_error = 0

if 'Q33313196' in wikidata_repet_id_dict:
    print(wikidata_repet_id_dict['Q33313196'])

# i = 0

# for key, value in bibkg_repeats_in_wikidata.items():
#     print(key)
#     print(value)
#     i += 1
#     if i > 100:
#         break

count_isbn = 0
count_properties_dict = {}
count_corr = 0

count_errors = 0

count_total_corr = 0
with open(archivo_json, 'r') as archivo:
    for linea in archivo:
        entity = json.loads(linea)
        id = entity['id']
        # if id == 'r_cn_Kilpatrick14':
        #     print(entity)
        #     break
        if '_corr_' in id:
            count_total_corr += 1 
        if id in wikidata_repet_id_dict:
            if '_corr_' in id:
                count_corr += 1
            for property in entity:
                count_properties_dict[property] = count_properties_dict.setdefault(property, 0) + 1
            
        if 'type' in entity:
            type = entity['type']
        else:
            type = 'unknown'
        if id in wikidata_repet_id_dict:
            count_wikidata_error_types[type] = count_wikidata_error_types.setdefault(type, 0) + 1
            print(id)
            print(wikidata_repet_id_dict[id])

            count_errors += 1
            # if 'isbn' in entity:
            #     print(entity['id'])
            #     print(" - ")
            #     print(wikidata_repet_id_dict[id])
            #     print(bibkg_repeats_in_wikidata[wikidata_repet_id_dict[id]])
            # if type == 'Article':
            #     print('Article: {} : {}'.format(id, wikidata_repet_id_dict[id]))
            #     count_article_error += 1
            #     if count_article_error > 10:
            #         break
            # # if type == 'Person':
            #     print('Person: {} : {}'.format(id, wikidata_repet_id_dict[id]))
            # elif type == 'Book':
            #     print('Book: {} : {}'.format(id, wikidata_repet_id_dict[id]))
            # elif type == 'Incollection':
            #     print('Incollection: {} : {}'.format(id, wikidata_repet_id_dict[id]))


# print(count_bibkg_id_repetitions)
# print(count_wikidata_id_repetitions)
print(count_wikidata_error_types)

# print(count_properties_dict)

# c = 0
# for key, val in wikidata_repet_id_dict.items():
#     print(key + ' : ' + val)
#     c += 1
#     if c > 20:
#         break

print(count_errors)

# print(count_corr)
# print(count_linked_corr)
# print(count_total_corr)