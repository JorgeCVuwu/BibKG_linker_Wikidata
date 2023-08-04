import json 
import time

def process_url(url):
    #print(url)
    # if 'anthology' in url:
    #     print(url)
    split = url.split('/')
    if split[0] != 'db':
        return False
    url1 = ''
    n = len(split) - 1
    for i in range(1, n):
        url1 += split[i] + '/'
    url_last = split[-1]
    if '#' in url_last:
        url_name =url_last.split('#')[1]
    else:
        url_name = url_last.replace(".html", "")
    dblp_id = url1 + url_name
    return dblp_id

def sumar_dict(dictionary, type):
        if type not in dictionary:
            dictionary[type] = 0
        dictionary[type] += 1


folder = "db/JSON/"
bibkg_url = folder + "bibkg.json"


count_entities = 0
count_urls = 0
count_type_dict = {}

count_type_url_dict = {}

count_dict_url_start = {}

count_url_db = {}
inicio = time.time()
with open(bibkg_url, 'r') as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if 'type' in entity:
            type = entity['type']
        else:
            type = 'unknown'
        sumar_dict(count_type_dict, type)
        count_entities += 1
        if ':url' in entity:
            #print(entity)
            try:
                sumar_dict(count_type_url_dict, type)
                if entity[':url'][0]['value'][0:3] == 'db/':
                    sumar_dict(count_url_db, type)
            except Exception as e:
                print(e)
                print(entity)
                print(entity[':url'])
                break
                
fin = time.time()
print("Tiempo de ejecución: {} segundos".format(fin - inicio))

print(count_type_dict)
print(count_type_url_dict)
print(count_dict_url_start)
print(count_url_db)

total_db = 0
for key, value in count_url_db.items():
    total_db += value
print(total_db)





