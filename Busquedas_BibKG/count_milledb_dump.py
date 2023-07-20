import json
import time
import re

def int_float(n):
    if n[-1:] == ".":
        n = n[:-1]
    valor = float(n)
    if valor.is_integer():
        return int(n)
    else:
        return valor
    
start = time.time()
count = 1
total = 144779468

bibkg_dictionary = {}

label_repeat_counts = {}

count_person = 0
count_person_2 = 0
count_person_3 = 0
count_person_4 = 0
count_person_5 = 0
count_person_6 = 0
count_person_7 = 0
c = 0
# Abre un archivo en modo escritura
with open("db/milledb/milleDB.dump", encoding="utf8") as milldb_file:
    for line in milldb_file:
        print(line)
        c += 1
        if c > 50:
            break

# print("\nCreando lista de diccionarios")
# lista_diccionarios = [v for k, v in bibkg_dictionary.items()]
# with open("bibkg_3.json", "w") as f:
#     print("creando archivo json")
#     json.dump(lista_diccionarios, f)
#     print("Archivo creado exitosamente")
# # with open("bibkgtest2.json", "w") as outfile:
# #     print("creando archivo json")
# #     json.dump(bibkg_dictionary, outfile)
# #     print("Archivo creado exitosamente")