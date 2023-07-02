import json 
import time

folder = "db/JSON/"

bibkg_url = folder + "bibkg linked by id.json"


count_dict = {}
type_dict = {}
c = 0
inicio = time.time()
with open(bibkg_url, 'r') as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'type' in entity:
            type = entity['type']
        else:
            type = 'unknown'
        if 'in_journal' in entity:
            n = str(len(entity['in_journal']))
            if n not in count_dict:
                count_dict[n] = 0
            count_dict[n] += 1
            if type not in type_dict:
                type_dict[type] = 0
            type_dict[type] += 1


fin = time.time()
print(count_dict)
print(type_dict)