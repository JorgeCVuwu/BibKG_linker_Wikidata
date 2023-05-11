import json

c = True

bibkg_part1_url = 'bibkg_part1.json'
bibkg_part2_url = 'bibkg_part2.json'
bibkg_part3_url = 'bibkg_part3.json'
bibkg_part4_url = 'bibkg_part4.json'

i_urls = [bibkg_part1_url, bibkg_part2_url, bibkg_part3_url, bibkg_part4_url]

bibkg_p1_url = 'bibkg_1.json'
bibkg_p2_url = 'bibkg_2.json'
bibkg_p3_url = 'bibkg_3.json'
bibkg_p4_url = 'bibkg_4.json'

o_urls = [bibkg_p1_url, bibkg_p2_url, bibkg_p3_url, bibkg_p4_url]

# Cargar el archivo JSON en memoria

for i in range(4):
    if i < 3:
        continue
    print("Iniciando carga de la parte {}".format(i + 1))
    with open(i_urls[i], 'r') as f:
        lista_objetos = json.load(f)

    # Escribir los objetos en el archivo JSON de salida

    print("Escribiendo parte {}".format(i + 1))
    with open(o_urls[i], 'w') as f:
        for i, objeto in enumerate(lista_objetos):
            # Escribir el objeto en el archivo de salida
            json.dump(objeto, f)
            f.write('\n')
            # if c:
            #     #print(ujson.dumps(objeto))
            #     c = False
            # Escribir un espacio después de cada objeto, excepto el último