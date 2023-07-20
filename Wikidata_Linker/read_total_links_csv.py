import csv
import json

archivo_json = 'db/JSON/bibkg.json'
archivo_csv = 'data/wikidata_linker/linked-entities-4.csv'
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
        if '###' in fila[2]:
            count_hashtags += 1
        wikidata_id = fila[1]
        # if bibkg_id == 'a_Nicholas_J__Dobbins':
        #     print(fila)
        #     print("adskfljgwkjfdshgeasrh")
        if wikidata_id == 'Q2644293':
            print(fila)
            print("a")
        bibkg_id_dict.setdefault(bibkg_id,[])
        bibkg_id_dict[bibkg_id].append(wikidata_id)
        wikidata_id_dict.setdefault(wikidata_id,[])
        wikidata_id_dict[wikidata_id].append(bibkg_id)
        if '_corr_' in bibkg_id:
            count_linked_corr += 1

count_repeated_bibkg_ids = 0
for key, value in bibkg_id_dict.items():
    if len(value) > 1:
        count_repeated_bibkg_ids += 1

count_repeated_wikidata_ids = 0
for key, value in wikidata_id_dict.items():
    if len(value) > 1:
        count_repeated_wikidata_ids += 1

count_bibkg_with_repeated_wikidata = 0
count_journal_repeated_ids = 0
max_entities_wikidata = 0
max_entities_wikidata_number = 0
repeated_wikidata_ids_list = {}
for key, value in wikidata_id_dict.items():
    n = len(value)
    if n > 1:
        repeated_wikidata_ids_list[key] = True
        count_bibkg_with_repeated_wikidata += n
        if n > max_entities_wikidata_number:
            max_entities_wikidata_number = n
            max_entities_wikidata = key
    
    # if len(value) > 20:
    #     print(key)
    #     print(value)
    #     break

count_wikidata_repets_dict = {}
count_corr = 0
count_id_and = 0
count_not_journal = 0
count_author_rep = 0
count_journal_and_else = 0
count_journal = 0
count_author_and_pub = 0

c = 0
first_row = []
count_first_link_dict = {}
with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    # Iterar sobre cada línea del archivo CSV
    first_row_bool = True
    for fila in lector_csv:
        if first_row_bool:
            first_row = fila
            first_row_bool = False
        else:
            bibkg_id = fila[0]
            wikidata_id = fila[1]

            # if fila[2]:
            #     #print(fila)
            #     c+=1
            #     if c > 10:
            #         break

            for i in range(4, len(first_row)):
                if fila[i]:
                    count_first_link_dict[first_row[i]] = count_first_link_dict.setdefault(first_row[i], 0) + 1
                    break

            if wikidata_id in repeated_wikidata_ids_list:
                if (fila[6] or fila[10]) and (fila[4] or fila[7] or fila[5] or fila[9] or fila[8] or fila[11]):
                    count_journal_and_else += 1
                    count_author_and_pub += 1
                if '_corr' in bibkg_id and not (fila[6] or fila[10]):
                    #print(fila)
                    # c+= 1
                    # if c > 10:
                    #     break
                    # break
                    count_corr += 1
                # if fila[4] or fila[8]:
                #     print(fila)
                #     c+= 1
                #     if c > 10:
                #         break
                #     break
                #     count_id_and += 1

                if fila[5] or fila[9]:
                    count_author_rep += 1

                if not (fila[6] or fila[10]):
                    count_not_journal += 1
                if fila[6] or fila[10]:
                    count_journal += 1
                for i in range(4, len(fila)):
                    value = fila[i]
                    if value:
                        count_wikidata_repets_dict[i] = count_wikidata_repets_dict.setdefault(i, 0) + 1
                        if i == 5:
                            if c < 10:
                                print(fila)
                            c+=1

count_type_dict = {}
count_type_linked_dict = {}
count_already_linked = 0
count_already_linked_people = 0
with open(archivo_json) as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'wikidata' in entity:
            count_already_linked += 1
            
        if 'type' in entity:
            entity_type = entity['type']
        else:
            entity_type = 'unknown'
        count_type_dict[entity_type] = count_type_dict.setdefault(entity_type, 0) + 1
        if id in bibkg_id_dict:
            if 'wikidata' not in entity:
                count_type_linked_dict[entity_type] = count_type_linked_dict.setdefault(entity_type, 0) + 1
            else:
                count_already_linked_people += 1



print("N° of repeated BibKG IDs: {}".format(count_repeated_bibkg_ids))
print("N° of repeated Wikidata IDs: {}".format(count_repeated_wikidata_ids))
print("N° of BibKG IDs with repeated Wikidata IDs: {}".format(count_bibkg_with_repeated_wikidata))

print("Wikidata ID with most BibKG IDs linked: {}, {} entities linked".format(max_entities_wikidata, max_entities_wikidata_number))

print(count_wikidata_repets_dict)
print(count_id_and)
print(count_not_journal)
print(count_author_rep)
print(count_author_and_pub)
print(count_journal)
print(count_first_link_dict)

print(count_type_dict)
print(count_type_linked_dict)
print(count_already_linked)
print(count_already_linked_people)


