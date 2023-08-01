import json

# Ruta y nombre del archivo de salida fusionado
folder = 'D:\Memoria'
archivo_fusionado = folder + '\wikidata_fusion.json'

# Ruta y nombres de los archivos de entrada
archivo1 = folder + '\wikidata_scholar_4.json'
archivo2 = folder + '\wikidata_else_4.json'

# Leer el contenido del archivo 1 y escribirlo en el archivo fusionado
with open(archivo1, 'r') as file1, open(archivo_fusionado, 'w') as output_file:
    for line in file1:
        output_file.write(line)
        #output_file.write('\n')
    output_file.write('\n')

# Leer el contenido del archivo 2 y escribirlo en el archivo fusionado (agregando al final)
with open(archivo2, 'r') as file2, open(archivo_fusionado, 'a') as output_file:
    for line in file2:
        output_file.write(line)
        #output_file.write('\n')