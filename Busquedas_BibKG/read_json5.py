import json
import os
import time
from urllib.parse import urlparse
import csv
import ujson
import datetime

def compare_year(date, end_point_year):
    n = len(date)
    if date[0] == "-":
        return False
    for i in range(n):
        char = date[i]
        if char == "-":
            index = i
            break
    year = date[:index]
    if int(year) < end_point_year:
        return False
    else:
        return True


bibkg_url = "bibkg.json"

carpeta_externa = "D:\Memoria" 

wikidata_person_file = "wikidata_person_3.json"
wikidata_scholar_file = "wikidata_scholar_3.json"
wikidata_else_file = "wikidata_else_3.json"
wikidata_filtered_person_file = "wikidata_person_filtered.json"

wikidata_person_csv_file = "wikidata_person_counts.csv"

wikidata_person_url = os.path.join(carpeta_externa, wikidata_person_file)
wikidata_scholar_url = os.path.join(carpeta_externa, wikidata_scholar_file)
wikidata_else_url = os.path.join(carpeta_externa, wikidata_else_file)

wikidata_person_filtered_url = os.path.join(carpeta_externa, wikidata_filtered_person_file)
wikidata_person_csv_url = os.path.join(carpeta_externa, wikidata_person_csv_file)

filename = wikidata_person_url
new_person_filename = os.path.join(carpeta_externa, '')

c = 0
inicio = time.time()


person_dict = {}

total = 0

count_publication_date = 0
count_before = 0
count_after = 0
count_unknown = 0

count_scholarly = 0
c = 0
with open(wikidata_scholar_url, 'r') as archivo_json:
    for linea in archivo_json:
        diccionario = json.loads(linea)
        claims = diccionario['claims']
        # for valor in claims['P31']:
        #     value = valor['mainsnak']['datavalue']['value']
        #     if value == 'Q13442814':
        #         count_scholarly += 1
        #         break

        if 'P577' in claims:
            count_publication_date += 1
            try:
                date = claims['P577'][0]['mainsnak']['datavalue']['value']['time']
                if compare_year(date, 1960):
                    count_after += 1
                else:
                    count_before += 1
            except:
                count_unknown += 1

        total += 1
        # if total > 100000:
        #     break

print(total)
print(count_publication_date)
print(count_before)
print(count_after)
print(count_unknown)


#P570