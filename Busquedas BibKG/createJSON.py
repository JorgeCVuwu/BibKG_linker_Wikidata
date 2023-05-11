import json
import time
import re
import traceback


def int_float(n):
    if n[-1:] == ".":
        n = n[:-1]
    valor = float(n)
    if valor.is_integer():
        return int(n)
    else:
        return valor
    
start = time.time()


write_urls = ["bibkg_part1.json", "bibkg_part2.json", "bibkg_part3.json", "bibkg_part4.json"]

# Abre un archivo en modo escritura
input_url = "milleDB.dump"
def read_and_write_file(input_url, write_urls, limit = 144000000):
    n_of_parts = len(write_urls)
    segment_size = limit/n_of_parts
    for z in range(n_of_parts):
        if z == 2:
            continue
        write_url = write_urls[z]
        with open(input_url, encoding="utf8") as milldb_file:
            count = 1

            count_actuals = 0

            bibkg_dictionary = {}

            try:
                for line in milldb_file:
                    if count <= z*segment_size:
                        count += 1
                        continue
                    splits = line.split()
                    link = splits[0]
                    if "->" in link:
                        #print(linked)
                        orden_bool = False
                        pos = link.find("->")
                        next_pos = pos + 1
                        link_components = link.split("->")
                        id = link_components[0]
                        if line[next_pos + 1] == "\"":
                            #print(line)
                            next_pos += 2
                            while next_pos < len(line) and line[next_pos] != "\"":
                                next_pos += 1
                                #print("sadfasfa")
                            link_to = line[(pos + 3):next_pos]
                            # print("Link to: " + link_to)
                            substrings = line[(next_pos + 1):].split()
                            property = substrings[0]
                            if len(substrings) == 2:
                                patron = r'\d+'
                                orden = substrings[1]
                                orden_bool = True
                                try:
                                    orden = re.search(patron, orden).group(0)
                                except:
                                    pass
                        else:
                            link_to = link_components[1]
                            property = splits[1].strip().strip(":")
                            if len(splits) == 3:
                                patron = r'\d+'
                                orden_bool = True
                                try:
                                    orden = re.search(patron, splits[2]).group(0)
                                except:
                                    orden = splits[2]
                        if "\"" in link_to:
                            link_to = link_to.replace("\"", "")
                        if id not in bibkg_dictionary:
                            #bibkg_dictionary[links[0]] = {}
                            bibkg_dictionary[id] = {'id':id}
                        if property != 'author_of':
                            if property not in bibkg_dictionary[id]:
                                bibkg_dictionary[id][property] = []
                            property_object = {'value':link_to}

                            if orden_bool:
                                property_object['orden'] = orden

                            bibkg_dictionary[id][property].append(property_object)
                            
                    else:
                        i = 0
                        j = 1
                        while line[j] != '\n':
                            while line[j] != " " and line[j] != "\n":
                                j+=1
                            substr = line[i:j]
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
                                bibkg_dictionary[object_name]['type'] = substr[1:]
                            else:
                                count_comillas = substr.count("\"")
                                if count_comillas>0 and count_comillas<2:
                                    #print(line)
                                    while line[j] != "\"":
                                        j+=1
                                        #print(line[j])
                                    j+=1
                                    substr = line[i:j]
                                    divisions = substr.split("\"")
                                    #print(line)
                                    #print(divisions)
                                    index = divisions[0] 
                                    if index[0] == " " or index[0] == ":":
                                        index = index[1:]
                                    #bibkg_dictionary[object_name][index[:-1]] = divisions[1]
                                    bibkg_dictionary[object_name][index[:-1]] = divisions[1]
                                
                                elif count_comillas == 2:
                                    separate = substr.split('\"')
                                    index = separate[0]
                                    if index[0] == " " or index[0] == ":":
                                        index = index[1:]
                                    #bibkg_dictionary[object_name][index[:-1]] = separate[1]     
                                    bibkg_dictionary[object_name][index[:-1]] = separate[1]                   
                                else:
                                    #print(substr)
                                    separate = substr.split(':')
                                    index = separate[0]
                                    if index[0] == " ":
                                        index = index[1:]
                                    #bibkg_dictionary[object_name][separate[0]] = float(separate[1])
                                    bibkg_dictionary[object_name][index] = int_float(separate[1])
                            i = j
                            j+=1
                            try:
                                line[j]
                            except IndexError:
                                break
                    #print("\rporcentaje: " + str(round((count/total)*100, 2)) + "%", end='')            
                    count += 1
                    if count%1000000 == 0:
                        print(count)  
                    if (z + 1) != n_of_parts:
                        if count > (z + 1)*segment_size:
                            break
                    
            except Exception as e:
                print(e)
                print("line " + str(count))
                print(line)
                traceback.print_exc()

        print("\nEscribiendo archivo {}".format(z + 1))
        with open(write_url, "w") as f:
            for key, valor in bibkg_dictionary.items():
                json.dump(valor, f)
                f.write('\n')
            # with open("bibkg_part4.json", "w") as f:
            #     print("creando archivo json")
            #     json.dump(lista_diccionarios, f)
            #     print("Archivo creado exitosamente")
            print("\nArchivo {} escrito".format(z + 1))

        print(count)
        print(count_actuals)


read_and_write_file(input_url, write_urls)