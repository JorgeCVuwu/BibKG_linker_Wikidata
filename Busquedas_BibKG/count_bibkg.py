import json 
import time
import csv

folder = "db/JSON/"

bibkg_url = folder + "bibkg.json"

c1 = 0
count_property_dict = {}


c = 0
inicio = time.time()
with open(bibkg_url, 'r') as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'has_author' in entity:
            print(entity['has_author'])
fin = time.time()

print("Tiempo de ejecución: {}".format(fin - inicio))
