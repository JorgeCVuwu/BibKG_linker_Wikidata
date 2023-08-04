import json
import time
import pickle

count = 0
count_autores = 0
count_article = 0
count_journal = 0
count_person = 0
count_person_puntos = 0
count_wikidata_puntos = 0
count_article_puntos = 0
count_field = 0
count_autores_10 = 0
count_entidades = 0
count_wikidata = 0
dict_wikidata = {}

# Intenta cargar el objeto JSON desde el archivo binario
try:
    with open('bibkg.bin', 'rb') as f:
        objetos = pickle.load(f)

# Si el archivo binario no existe, carga el objeto JSON desde el archivo JSON
except FileNotFoundError:
    with open('bibkg_2.json', 'r') as f:
        #data = json.load(f)
        for linea in f:
            inicio2 = time.time()
            # Intenta cargar el objeto JSON desde el archivo binario
            objetos = json.loads(linea)
            #objetos = json.loads(linea)
            fin2 = time.time()
            print("JSON cargado. Tiempo de carga: " + str(fin2 - inicio2) + " segundos")

    # Guarda el objeto JSON en un archivo binario para futuras consultas
    with open('bibkg.bin', 'wb') as f:
        pickle.dump(objetos, f)


        # for objeto in objetos:
        #     # Si el atributo "id" tiene el valor buscado, imprimir el objeto JSON completo
        #     try:
        #         # if objeto['id'] == 't_meltdown_s18':
        #         #     print(objeto)
        #         #     break_cond = True
        #         #     break
        #         if "id" in objeto:
        #             if objeto["id"] == "a_Aidan_Hogan":
        #                 print(objeto)
        #         if "has_author" in objeto:
        #             n_autores = len(objeto["has_author"])
        #             if n_autores >= 10:
        #                 count_autores_10+=1
        #         # print("\rcount: " + str(count), end='')  
        #         # count += 1
        #         # if "wikidata" in objeto:
        #         #     count_wikidata += 1
        #         #     tipo = objeto["type"]
        #         #     if tipo not in dict_wikidata:
        #         #         dict_wikidata[tipo] = 0
        #         #     dict_wikidata[tipo] += 1
        #         # if " wikidata" in objeto:
        #         #     count_wikidata += 1
        #         # if "type" in objeto:
        #         #     if objeto["type"] == "Article":
        #         #         count_article += 1
        #         #     if objeto["type"] == " Article":
        #         #         count_article_puntos += 1
        #         #     if objeto["type"] == "Field":
        #         #         count_field += 1
        #         #     if objeto["type"] == "Journal":
        #         #         count_journal += 1
        #         #     if objeto["type"] == "Person":
        #         #         count_person += 1  
        #         #     if objeto["type"] == " Person":
        #         #         count_person_puntos += 1                        
        #         count_entidades += 1
        #     except Exception as e:
        #         fin = time.time()
        #         print(e)
        #         print("Error, segundos transcurridos: " + str(fin - inicio))
        #         break
        # if break_cond:
        #     break
    fin = time.time()
    # print("Número de publicaciones con 10 o más autores: " + str(count_autores_10))
    # print("Número de entidades de BibKG: " + str(count_entidades))
    # print("Numero de artículos: " + str(count_article))
    # print("Numero de :artículos: " + str(count_article_puntos))
    # print("Numero de journals: " + str(count_journal))
    # print("Numero de fields: " + str(count_field))
    # print("Numero de objetos del tipo Person: " + str(count_person))
    # print("Numero de objetos del tipo :Person: " + str(count_person_puntos))
    # print("Numero de referencias a Wikidata: " + str(count_wikidata))
    # print("Numero de referencias a :Wikidata: " + str(count_wikidata_puntos))
    # print("Counts de Wikidata: ")
    # print(dict_wikidata)
    # print("Tiempo de lectura de consulta a archivo JSON: " + str(fin - inicio) + " segundos")
    # while True:
    #     entrada = input("Quieres introducir código? y/n ")
    #     if entrada == "y":
    #         print("Llamando al subproceso")
    #         subprocess.call(['python', 'read_json2.py'] + objetos)
    #     elif entrada == "n":
    #         break
    #     else:
    #         print("Por favor, introduce algo válido")
            

    