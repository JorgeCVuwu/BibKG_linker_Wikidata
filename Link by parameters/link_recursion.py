from link_authors import link_authors
from link_publications import link_publications
import json
import re
import time
import os
import csv

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg linked by id.json"
bibkg_names_path = json_folder + "bibkg_person_name.json"
bibkg_linked_path_authors = json_folder + "bibkg linked authors.json"
bibkg_linked_path_publications = json_folder + "bibkg linked publications.json"

carpeta_externa = "D:\Memoria" 
wikidata_person_name = "wikidata_person_4.json"
wikidata_scholar_name = "wikidata_scholar_4.json"

wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

total_links_writed = 0

count_links_writed = 1

total_recursions = 0

inicio = time.time()

while count_links_writed != 0:

    count_links_writed = link_authors(bibkg_path, bibkg_linked_path_authors, wikidata_person_path, wikidata_scholar_path)
    total_links_writed += count_links_writed

    print("Enlaces escritos por link_authors: {}".format(count_links_writed))

    count_links_writed = link_publications(bibkg_linked_path_authors, bibkg_linked_path_publications, wikidata_person_path, wikidata_scholar_path)
    total_links_writed += count_links_writed

    bibkg_path = bibkg_linked_path_publications

    print("Enlaces escritos por link_publications: {}".format(count_links_writed))

    total_recursions += 1

fin = time.time()

print("Guardando metadatos")

data = [
    ['time_hours', 'writed_linked_entities', 'total_recursions'],
    [(fin - inicio)/3600, total_links_writed, total_recursions]
]
csv_folder = "Link by parameters/data/"
metadata_path = csv_folder + 'link-recursion-metadata.csv'
with open(metadata_path, mode='w', newline='') as archivo_csv:
    
    # Crea el objeto de escritura de CSV
    writer = csv.writer(archivo_csv)
    
    # Escriba los datos en el archivo CSV
    for fila in data:
        writer.writerow(fila)

print("Enlaces totales escritos: {}".format(total_links_writed))
print("Recursiones totales del proceso: {}".format(total_recursions))

print("Tiempo total de ejecución de la recursión: {}".format(fin - inicio))