import ujson
import json
import os 

carpeta_externa = "D:\Memoria" 

file = os.path.join(carpeta_externa, "wikidata_scholar.json")

# folder = 'Wikidata parser/'
# file = 'bibkg_2.json'
path = file
with open(path, 'r') as f:
    # Lee la primera línea para obtener el corchete izquierdo "["
    linea = f.readline().strip()
    # Si la primera línea no tiene el corchete izquierdo "[", lanzar una excepción
    if not linea.startswith('['):
        raise ValueError('El archivo no comienza con un corchete izquierdo "["')
    obj = json.loads(linea[1:].strip(',\n'))
    print(linea)
    
    # Lee cada línea del archivo excepto la primera y la última
    for linea in f:
        # Carga el objeto JSON en una variable
        obj = json.loads(linea.strip(',\n'))
        # Usa el objeto como desees
        print(obj)
        break
    # Lee la última línea para obtener la coma "," y el corchete derecho "]"
    linea = linea.strip()
    # Si la última línea no tiene la coma "," y el corchete derecho "]", lanzar una excepción
    if not linea.endswith(']'):
        raise ValueError('El archivo no termina con una coma "," y un corchete derecho "]"')
    obj = json.loads(linea.strip(']'))