import time
import ujson

count = 0
with open("wikidata_person.json", "r") as file:
        for linea in file:
            inicio2 = time.time()
            # Intenta cargar el objeto JSON desde la línea actual
            try:
                objeto = ujson.loads(linea)
                break
            except ujson.JSONDecodeError:
                print("Error de decodificación en la línea: " + linea)
                continue
            
            fin2 = time.time()
            #print("JSON cargado. Tiempo de carga: " + str(fin2 - inicio2) + " segundos")

count2 = 0
count3 = 0
list_keys = []
print(objeto['claims']['P509'][0]['mainsnak']['datatype'])
claims = objeto['claims']        
for llave in claims:
    for valor in claims[llave]:
    #print(valor)
        datatype = valor['mainsnak']['datatype']
        if datatype == "external-id":
                count += 1
                list_keys.append(llave)

for v in objeto:
    print(v)

#print(objeto["description"])
print(count)
# print(count2)
# print(count3)
#print(claims['P6262'])
# for v in claims['P6262']:
#      print(v)
#      print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#ass =  in list_keys
#print(ass)