import json

c = True
# Cargar el archivo JSON en memoria
with open('Wikidata parser/bibkg_2.json', 'r') as f:
    lista_objetos = json.load(f)

# Escribir los objetos en el archivo JSON de salida
with open('bibkg.json', 'w') as f:
    for i, objeto in enumerate(lista_objetos):
        # Escribir el objeto en el archivo de salida
        f.write(json.dumps(objeto))
        if c:
            print(json.dumps(objeto))
            c = False
        # Escribir un espacio después de cada objeto, excepto el último
        if i < len(lista_objetos) - 1:
            f.write('\n')