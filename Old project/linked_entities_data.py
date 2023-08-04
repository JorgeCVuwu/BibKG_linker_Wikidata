import csv
import os
import json

carpeta_externa = "D:\Memoria" 

metadata_path = os.path.join(carpeta_externa, 'recursion-linked-entities.csv')

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg.json"

bibkg_linked_entities = {}
count_link_types_dict = {}
count_entity_types_dict = {'total':0}
count_repeated_entities = 0
repeated_entities_dict = {}
repeated_entities_type_dict = {}
repeated_entities_link_type_dict = {}

# Abre el archivo CSV en modo lectura
with open(metadata_path, 'r') as archivo_csv:
    # Crea un objeto lector CSV
    lector_csv = csv.reader(archivo_csv)
    # Lee el contenido del archivo fila por fila
    for fila in lector_csv:
        # Cada fila se trata como una lista de valores
        # Accede a los valores individuales utilizando índices
        bibkg_entity_id = fila[0]
        #wikidata_entity_id = fila[1]
        link_type = fila[2]
        
        if link_type not in count_link_types_dict:
            count_link_types_dict[link_type] = 0
        count_link_types_dict[link_type] += 1
        if bibkg_entity_id in bibkg_linked_entities:
            count_repeated_entities += 1
            repeated_entities_dict[bibkg_entity_id] = True
            if link_type not in repeated_entities_link_type_dict:
                repeated_entities_link_type_dict[link_type] = 0
            repeated_entities_link_type_dict[link_type] += 1
        bibkg_linked_entities[bibkg_entity_id] = True

        # Haz algo con los valores leídos

with open(bibkg_path, 'r') as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'type' in entity:
            type = entity['type']
        else:
            type = 'unknown'
        if id in bibkg_linked_entities:
            if type not in count_entity_types_dict:
                count_entity_types_dict[type] = 0
            count_entity_types_dict[type] += 1
            count_entity_types_dict['total'] += 1
        if id in repeated_entities_dict:
            if type not in repeated_entities_type_dict:
                repeated_entities_type_dict[type] = 0
            repeated_entities_type_dict[type] += 1

print(count_link_types_dict)
print(count_entity_types_dict) 
print(count_repeated_entities)
print(repeated_entities_type_dict)
print(repeated_entities_link_type_dict)