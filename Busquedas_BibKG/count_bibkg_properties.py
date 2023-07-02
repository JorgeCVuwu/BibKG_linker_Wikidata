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
        for property in entity:
            if property not in count_property_dict:
                count_property_dict[property] = 0
            count_property_dict[property] += 1
        c1 += 1

print("Guardando metadatos")

data = [
    ['BibKG property', 'count'],
]

propiedades_ordenadas = {k: v for k, v in sorted(count_property_dict.items(), key=lambda item: item[1], reverse=True)}

for key, value in propiedades_ordenadas.items():
    data.append([key, value])

csv_folder = "Busquedas_BibKG/data/"
metadata_path = csv_folder + 'count-bibkg-properties.csv'
with open(metadata_path, mode='w', newline='') as archivo_csv:
    
    # Crea el objeto de escritura de CSV
    writer = csv.writer(archivo_csv)
    
    # Escriba los datos en el archivo CSV
    for fila in data:
        writer.writerow(fila)



fin = time.time()

print("Tiempo de ejecución: {}".format(fin - inicio))
