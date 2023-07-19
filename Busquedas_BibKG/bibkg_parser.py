import json
import time
import re
import os

def int_float(n):
    if n[-1:] == ".":
        n = n[:-1]
    valor = float(n)
    if valor.is_integer():
        return int(n)
    else:
        return valor

class BibKGParser():
    
    def __init__(self, parts_list):
        self.write_urls = parts_list
        self.bibkg_path = "bibkg_copy.json"
        self.input_url = "db/milledb/milleDB.dump"
        self.folder = "db/JSON/"
        self.limit = 144000000
        self.bibkg_dictionary = {}


    #add_to_entity_dict: se almacena la cantidad de veces que es aludida una entidad como elemento principal de la línea
    #(o sea, la entidad a la que se define en la línea, o la entidad a la que se le añade un nuevo valor en una propiedad)
    def add_to_entity_dict(self, path):
        with open(path, 'r') as bibkg:
            for linea in bibkg:
                entity = json.loads(linea)
                id = entity['id']
                self.entity_dict.setdefault(id, 0)
                self.entity_dict[id] += 1


    #write_new_part: Escribe las entidades y propiedades no repetidas en el archivo JSON nuevo
    def write_new_part(self, bibkg, part_path):
        part_path = part_path
        with open(part_path, 'r') as p:
            for linea in p:
                entity = json.loads(linea)
                if 'author_of' in entity:
                    del entity['author_of']
                id = entity['id']
                if id not in self.repeated_dict:
                    json.dump(entity, bibkg)
                    bibkg.write('\n')
                else:
                    if id not in self.repeated_objects:
                        self.repeated_objects[id] = entity
                    else:
                        repeated_object = self.repeated_objects[id]
                        for key, value in entity.items():
                            if key in repeated_object and key != "id" and type(repeated_object[key]) == list:
                                for elemento in value:
                                    if elemento not in repeated_object[key]:
                                        self.repeated_objects[id][key].append(elemento)
                                # if key not in self.repeated_counts:
                                #     self.repeated_counts[key] = 0
                                # self.repeated_counts[key] += 1
                            else:
                                self.repeated_objects[id][key] = value
        os.remove(part_path)


    #merge_bibkg_parts: junta todas las partes de JSON de BibKG a un único archivo JSON
    #Está pensada para crear partes en potencias de 2 (1, 2, 4, 8...)
    def merge_bibkg_parts(self):
        print("Comenzando el proceso de unión de partes de BibKG")
        n = len(self.write_urls)
        count = 1
        self.entity_dict = {}
        self.repeated_dict = {}
        self.repeated_objects = {}

        for i in range(n):
            self.write_urls[i] = self.folder + self.write_urls[i]
        #self.repeated_counts = {}

        new_parts_path_list = []

        while len(self.write_urls) != 1:

            for i in range(0, n-1, 2):
                bibkg_path_1, bibkg_path_2 = self.write_urls[i], self.write_urls[i + 1]
                
                
                self.add_to_entity_dict(bibkg_path_1)
                self.add_to_entity_dict(bibkg_path_2)

                # c_repeated = 0

                for key, valor in self.entity_dict.items():
                    if valor > 1:
                        self.repeated_dict[key] = valor
                        #c_repeated += 1

                if len(self.write_urls) == 2:
                    new_bibkg_path = self.folder + self.bibkg_path
                    print("Escribiendo archivo JSON final")
                    new_parts_path_list = []
                else:
                    new_bibkg_path = self.folder + 'bibkg_' + str(count) + '.json'
                    print("Escribiendo archivo N°{}".format(count))
                    count += 1

                with open(new_bibkg_path, 'w') as bibkg:
                    self.write_new_part(bibkg, bibkg_path_1)
                    self.write_new_part(bibkg, bibkg_path_2)


                with open(new_bibkg_path, 'a') as bibkg:
                    for _, value in self.repeated_objects.items():
                        json.dump(value, bibkg)
                        bibkg.write('\n')
                    new_parts_path_list.append(new_bibkg_path)

                self.entity_dict = {}
                self.repeated_dict = {}
                self.repeated_objects = {}

            self.write_urls = new_parts_path_list
        #self.repeated_counts = {}
        

    #parse_bibkg: crea archivos JSON por partes a partir del archivo dump de BibKG
    def parse_bibkg(self):
        n_of_parts = len(self.write_urls)
        segment_size = self.limit/n_of_parts
        for z in range(n_of_parts):
            #reiniciar diccionario
            self.bibkg_dictionary = {}
            # if z == 2 or z == 3:
            #     continue
            with open(self.input_url, encoding="utf8") as milldb_file:
                count = 1

                count_actuals = 0
                for line in milldb_file:
                    if count <= z*segment_size:
                        count += 1
                        continue
                    #splits es cada segmento de la línea
                    splits = line.split()
                    link = splits[0]

                    #Casos de linea que indica una propiedad de una entidad (con los símbolos "->" al inicio)
                    if "->" in link:
                        orden_bool = False
                        #pos es el puntero dentro del string de la linea
                        pos = link.find("->")
                        next_pos = pos + 1
                        link_components = link.split("->")
                        id = link_components[0]
                        #Considerar todo lo que está adentro de unas comillas en el string ("") como el valor de la propiedad, de existir
                        if line[next_pos + 1] == "\"":
                            next_pos += 2
                            while next_pos < len(line) and line[next_pos] != "\"":
                                next_pos += 1
                            link_to = line[(pos + 3):next_pos]
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
                        if id not in self.bibkg_dictionary:
                            self.bibkg_dictionary[id] = {'id':id}
                        property = property.lstrip(':')
                        #No añadir las propiedades 'author_of' al diccionario para escribir
                        if property != 'author_of':
                            if property not in self.bibkg_dictionary[id]:
                                self.bibkg_dictionary[id][property] = []
                            property_object = {'value':link_to}

                            if orden_bool:
                                property_object['orden'] = orden

                            self.bibkg_dictionary[id][property].append(property_object)

                    else:
                        #i, j: punteros para leer la línea (el segmento substr está entre estas posiciones dentro de la línea)
                        i = 0
                        j = 1
                        #se lee mientras no acabe la línea
                        while line[j] != '\n':
                            #el puntero j será definido como la posición después de i que esté antes del próximo espacio o fin de línea 
                            while line[j] != " " and line[j] != "\n":
                                j+=1
                            substr = line[i:j]                    
                            j+=1
                            if i == 0:
                                object_name = substr
                                if object_name not in self.bibkg_dictionary:
                                    self.bibkg_dictionary[object_name] = {'id': object_name}

                            #Se define el tipo de la entidad cuando se encuentran dos puntos ':' al inicio de 
                            elif substr[0] == ":":
                                self.bibkg_dictionary[object_name]['type'] = substr[1:]
                            else:
                                count_comillas = substr.count("\"")
                                #Caso en que existan 1 o 2 comillas dentro del segmento
                                #Si se cuenta 1 comilla, significa que existe otra posteriormente, se aumenta j hasta encontrarla
                                #esto para los casos en que property:"hola que tal" (en estos casos existen espacios dentro del valor de la propiedad)
                                if count_comillas == 1 or count_comillas == 2:
                                    if count_comillas == 1:
                                        while line[j] != "\"":
                                            j+=1
                                        j+=1
                                        substr = line[i:j]
                                        #Se obtiene el valor dentro de las comillas
                                    divisions = substr.split("\"")

                                    index = divisions[0] 
                                    if index[0] == " " or index[0] == ":":
                                        index = index[1:]
                                    self.bibkg_dictionary[object_name][index[:-1]] = divisions[1]

                                else:
                                    separate = substr.split(':')
                                    index = separate[0]
                                    if index[0] == " ":
                                        index = index[1:]
                                    self.bibkg_dictionary[object_name][index] = int_float(separate[1])

                            #Avanzar al siguiente segmento
                            i = j
                            j+=1
                            try:
                                line[j]
                            except IndexError:
                                break

                    count += 1
                    if count%1000000 == 0:
                        print(count)  
                    if (z + 1) != n_of_parts:
                        if count > (z + 1)*segment_size:
                            break

            print("\nEscribiendo archivo {}".format(z + 1))
            write_url = self.folder + self.write_urls[z]

            #Escribir lo procesado en el archivo
            with open(write_url, "w") as f:
                for _, valor in self.bibkg_dictionary.items():
                    json.dump(valor, f)
                    f.write('\n')
                print("\nArchivo {} escrito".format(z + 1))



if __name__ == "__main__":
    inicio = time.time()

    parts_list = ["bibkg_part1.json", "bibkg_part2.json", "bibkg_part3.json", "bibkg_part4.json"]
    bibkg_parser = BibKGParser(parts_list)

    #bibkg_parser.parse_bibkg()
    bibkg_parser.merge_bibkg_parts()

    fin = time.time()

    print("Tiempo de ejecución: {} segundos".format(fin - inicio))