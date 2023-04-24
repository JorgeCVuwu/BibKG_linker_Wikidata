import json

# Abrir el archivo en modo lectura
with open('wikidata_scholar2.json', 'r') as f:
    # Cargar el contenido del archivo en un objeto Python
    datos = json.load(f)

# Imprimir el objeto Python
for v in datos[0]:
    print(v)
    print(datos[0][v])