import json
import time


count_wikidata = 0
count_person = 0

wikidata_dict = {}

with open('db/JSON/bibkg linked authors.json', 'r') as f:
    break_cond = False
    for linea in f:
        entity = json.loads(linea)
        id = entity['id']
        if 'type' in entity:
            type = entity['type']
        else:
            type = ''
        if 'wikidata' in entity:
            if type == 'Person':
                count_person += 1
                wikidata_id = entity['wikidata']
                wikidata_dict[wikidata_id] = wikidata_dict.setdefault(wikidata_id, 0) + 1
            count_wikidata += 1

count_repeated_wikidata_ids = 0
for key, value in wikidata_dict.items():
    if value > 1:
        count_repeated_wikidata_ids += 1

print(count_wikidata)
print(count_person)
print(count_repeated_wikidata_ids)
