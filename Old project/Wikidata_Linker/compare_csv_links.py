import csv


csv_1_bibkg_dict = {}
csv_2_bibkg_dict = {}

csv_data_header = [
            'bibkg_id', 'wikidata_id', 'previous_link', 'other_wikidata_ids', 'dblp_id', 'linked_by_id', 'linked_by_id_recursion_authors', 
            'linked_by_id_recursion_journals', 'linked_by_id_recursion_publications', 'linked_by_comparisons', 
            'linked_by_comparisons_recursion_authors',  'linked_by_comparisons_recursion_journals', 
            'linked_by_comparisons_recursion_publications'
        ]

archivo_csv_1 = 'data/wikidata_linker/linked-entities-5.csv'
archivo_csv_2 = 'data/wikidata_linker/linked-entities-6.csv'

count_new_links = 0
count_link_type_dict = {}

with open(archivo_csv_1, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:
        csv_1_bibkg_dict[fila[0]] = fila[1]
        csv_2_bibkg_dict[fila[1]] = fila[0]

with open(archivo_csv_2, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    
    # Iterar sobre cada línea del archivo CSV
    for fila in lector_csv:
        bibkg_id = fila[0]
        wikidata_id = fila[1]
        if bibkg_id not in csv_1_bibkg_dict and wikidata_id not in csv_2_bibkg_dict:
            count_new_links += 1
            for i in range(4, len(fila)):
                if fila[i]:
                    count_link_type_dict[csv_data_header[i]] = count_link_type_dict.setdefault(csv_data_header[i], 0) + 1
                    # if csv_data_header[i] == 'linked_by_id':
                    #     print(bibkg_id)
                    #     print(fila[1])
                    #     break


print(count_new_links)
print(count_link_type_dict)

