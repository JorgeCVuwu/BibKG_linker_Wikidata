import json
import os
import time
from urllib.parse import urlparse
import csv

def detect_page(url):
    parsed_url = urlparse(url)

    if parsed_url.scheme in ["http", "https"]:
        page_prefix = parsed_url.scheme + "://" + parsed_url.netloc
        page_suffix = parsed_url.path.lstrip("/")
    else:
        page_prefix = ""
        page_suffix = url
    return page_prefix, page_suffix

url1 = "https://doi.org/10.1145/1242572.1242819"
url2 = "https://spectreattack.com/spectre.pdf"

print(detect_page(url1))
print(detect_page(url2))



bibkg_url = "bibkg.json"

carpeta_externa = "D:\Memoria" 

wikidata_person_file = "wikidata_person_3.json"
wikidata_scholar_file = "wikidata_scholar_3.json"
wikidata_else_file = "wikidata_else_3.json"

wikidata_person_url = os.path.join(carpeta_externa, wikidata_person_file)
wikidata_scholar_url = os.path.join(carpeta_externa, wikidata_scholar_file)
wikidata_else_url = os.path.join(carpeta_externa, wikidata_else_file)

filename = bibkg_url

c = 0
inicio = time.time()
count_wikidata = 0
count_ee = 0
count_ee_dict = {}
with open(filename, 'r') as archivo_json:
    for linea in archivo_json:
        diccionario = json.loads(linea)
        if 'ee' in diccionario:
            count_ee += 1
            ee = diccionario['ee']
            prefix, _ = detect_page(ee)
            # if prefix == "http://arxiv.org":
            #     print(diccionario)
            #     break
            if prefix not in count_ee_dict:
                count_ee_dict[prefix] = 0
            count_ee_dict[prefix] += 1

        # print(diccionario)
        # print("AAAAAAAAAAAAAAAAAAA")
        # c += 1
        # if c > 10:
        #     break
    count_ee_dict['total'] = count_ee
fin = time.time()
print("Tiempo de ejecución: {} segundos".format(fin - inicio))
print(count_ee)
#print(count_ee_dict)

archivo_json.close()

folder = 'Link BibKG/data/'
metadata_path = folder + 'count-ee.csv'
with open(metadata_path, mode='w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(["Fuente", "Count"])
    sorted_items = sorted(count_ee_dict.items(), key=lambda x: x[1], reverse=True)
    for llave, numero in sorted_items:
        writer.writerow([llave, numero])
