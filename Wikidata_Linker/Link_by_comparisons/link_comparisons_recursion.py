import os
import csv
import time
from Link_by_id.link_by_id import link_by_id
from Link_by_parameters.link_authors import link_authors
from Link_by_parameters.link_publications import link_publications
from Link_by_comparisons.link_by_comparisons import link_by_comparisons

json_folder = "db/JSON/"
bibkg_path = json_folder + "bibkg.json"

carpeta_externa = "D:\Memoria" 
wikidata_person_name = "wikidata_person_4.json"
wikidata_scholar_name = "wikidata_scholar_4.json"

wikidata_person_path = os.path.join(carpeta_externa, wikidata_person_name)
wikidata_scholar_path = os.path.join(carpeta_externa, wikidata_scholar_name)

total_recursions = 0

total_links_writed = 0

count_links_writed = 1

writed_links_dict = {}

csv_data = [
    ['entity_id', 'wikidata_id', 'link_method']
]

inicio = time.time()

metadata_path = carpeta_externa + 'recursion-linked-entities.csv'
with open(metadata_path, mode='w', newline='') as archivo_csv:

    writed_links_dict, count_links_writed, csv_data = link_by_id(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict)
    total_links_writed += count_links_writed

    print("Enlazamiento por ID completado")
    print("Enlaces escritos conseguidos: {}".format(count_links_writed))
    print("Enlaces totales hasta el momento: {}".format(total_links_writed))

    count_links_writed = 1

    print("Inicio del bucle de relaciones a partir del ID")
    while count_links_writed != 0:
        writed_links_dict, count_links_writed, csv_data = link_authors(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict)
        total_links_writed += count_links_writed

        print("Enlaces escritos por link_authors: {}".format(count_links_writed))
        print("Enlaces totales hasta el momento: {}".format(total_links_writed))

        writed_links_dict, count_links_writed, csv_data = link_publications(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict)
        total_links_writed += count_links_writed

        print("Enlaces escritos por link_publications: {}".format(count_links_writed))
        print("Enlaces totales hasta el momento: {}".format(total_links_writed))

        total_recursions += 1

    print("Iniciando fase de enlazamiento por comparaciones de propiedades")

    writed_links_dict, count_links_writed, csv_data = link_by_comparisons(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict)
    total_links_writed += count_links_writed
    print("Enlaces escritos por link_by_comparisons: {}".format(count_links_writed))
    print("Enlaces totales hasta el momento: {}".format(total_links_writed))

    count_links_writed = 1

    print("Iniciando bucle a partir de enlaces por comparaciones:")
    while count_links_writed != 0:

        writed_links_dict, count_links_writed, csv_data = link_authors(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict, "linked_by_comparison_propagation")
        total_links_writed += count_links_writed

        print("Enlaces escritos por link_authors: {}".format(count_links_writed))
        print("Enlaces totales hasta el momento: {}".format(total_links_writed))

        writed_links_dict, count_links_writed, csv_data = link_publications(bibkg_path, wikidata_person_path, wikidata_scholar_path, csv_data, writed_links_dict, "linked_by_comparison_propagation")
        total_links_writed += count_links_writed

        print("Enlaces escritos por link_publications: {}".format(count_links_writed))
        print("Enlaces totales hasta el momento: {}".format(total_links_writed))

        total_recursions += 1

    fin = time.time()

    print("Enlaces totales escritos: {}".format(total_links_writed))
    print("Recursiones totales del proceso: {}".format(total_recursions))

    print("Guardando archivo CSV de entidades")

    writer = csv.writer(archivo_csv)
    for fila in csv_data:
        writer.writerow(fila)






print("Guardando metadatos")

data = [
    ['time_hours', 'writed_linked_entities', 'total_recursions'],
    [(fin - inicio)/3600, total_links_writed, total_recursions]
]

csv_folder = "Link_by_comparisons/data/"
metadata_path = csv_folder + 'link-recursion-metadata.csv'
with open(metadata_path, mode='w', newline='') as archivo_csv:
    
    # Crea el objeto de escritura de CSV
    writer = csv.writer(archivo_csv)
    
    # Escriba los datos en el archivo CSV
    for fila in data:
        writer.writerow(fila)


print("Tiempo total de ejecución del proceso completo: {}".format(fin - inicio))
print("Total de entidades enlazadas en el proceso: {}".format(total_links_writed))