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

# Abre un archivo en modo escritura
with open("milleDB.dump", encoding="utf8") as milldb_file:
    try:
        for line in milldb_file:
            splits = line.split()
            linked = splits[0]
            if splits[1] == ":Person":
                count_person_3 += 1
            if "->" in linked:
                pass
                # #print(linked)
                # links = linked.split("->")
                # if "\"" in links[1]:
                #     links[1] = links[1].replace("\"", "")
                # if links[0] not in bibkg_dictionary:
                #     #bibkg_dictionary[links[0]] = {}
                #     bibkg_dictionary[links[0]] = {'id':links[0]}
                # index = splits[1]
                # if index[0] != 'author_of':
                #     if index[0] == ":" or index[0] == " ":
                #         index = index[1:]
                #     if len(splits) == 3:
                #         patron = r'\d+'
                #         try:
                #             orden = re.search(patron, splits[2]).group(0)
                #         except:
                #             orden = splits[2]
                #         if index not in bibkg_dictionary[links[0]]:
                #             bibkg_dictionary[links[0]][index] = {}
                #         if orden in bibkg_dictionary[links[0]][index]:
                #             if line not in label_repeat_counts:
                #                 label_repeat_counts[line] = 2
                #             orden = orden + str(label_repeat_counts[line])
                #             bibkg_dictionary[links[0]][index][orden] = links[1]
                #             label_repeat_counts[line]+=1
                #         else:
                #             bibkg_dictionary[links[0]][index][orden] = links[1]
                    

                # else:
                #     bibkg_dictionary[links[0]][index] = links[1] 
                
            else:
                i = 0
                j = 1
                while line[j] != '\n':
                    while line[j] != " " and line[j] != "\n":
                        j+=1
                    substr = line[i:j]
                    if substr == ":Person":
                        count_person += 1
                    #print(substr)
                    j+=1
                    #print("substr = " + substr)
                    if i == 0:
                        object_name = substr
                        if object_name not in bibkg_dictionary:
                            #bibkg_dictionary[object_name] = {}
                            bibkg_dictionary[object_name] = {'id': object_name}
                            
                    elif substr[0] == ":":
                        #bibkg_dictionary[object_name]['type'] = substr[1:]
                        if "type" in bibkg_dictionary[object_name]:
                            count_person_4 += 1
                            if bibkg_dictionary[object_name]['type'] == "Person":
                                count_person_5 += 1
                        bibkg_dictionary[object_name]['type'] = substr[1:]
                        if substr == ":Person":
                            count_person_2 += 1
                    else:
                        pass
                        # count_comillas = substr.count("\"")
                        # if count_comillas>0 and count_comillas<2:
                        #     #print(line)
                        #     while line[j] != "\"":
                        #         j+=1
                        #         #print(line[j])
                        #     j+=1
                        #     substr = line[i:j]
                        #     divisions = substr.split("\"")
                        #     #print(line)
                        #     #print(divisions)
                        #     index = divisions[0] 
                        #     if index[0] == " " or index[0] == ":":
                        #         index = index[1:]
                        #     #bibkg_dictionary[object_name][index[:-1]] = divisions[1]
                        #     bibkg_dictionary[object_name][index[:-1]] = divisions[1]
                        
                    i = j
                    j+=1
                    try:
                        line[j]
                    except IndexError:
                        break
            #print("\rporcentaje: " + str(round((count/total)*100, 2)) + "%", end='')            
            count += 1  
            # if count > 100:
            #     break
            
    except Exception as e:
        print(e)
        print("line " + str(count))
        print(line)

print(count_person)
print(count_person_2)
print(count_person_3)
print(count_person_4)
print(count_person_5)

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