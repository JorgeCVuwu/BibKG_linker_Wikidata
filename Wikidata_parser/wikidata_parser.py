import gzip
import json
import time
import ujson
import os
import csv

#reduce_datavalue: simplifica o elimina algunos snaks de cierto tipo de Wikidata (según el tipo del snak (type))
def reduce_datavalue(datavalue):
    type = datavalue['type']
    if type == "string":
        return datavalue
    elif type == "wikibase-entityid":
        return {'value':datavalue['value']['id'], 'type':type}
    elif type == "globecoordinate" or type == "quantity":
        return {}
    elif type == "time":
        value = datavalue['value']
        return {'value':{'time':value['time'], 'precision':value['precision']}, 'type':type}
    else:
        return datavalue
    
#readCSV: lee un archivo CSV y toma todos los elementos de la primera columna
def readCSV(path):
    columna = 0
    filter_list = []
    with open(path, mode='r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            elemento = fila[columna]
            filter_list.append(elemento)
    return filter_list

#replaceWikidataHeader: quita los headers de las URLs de las entidades de Wikidata
def replaceWikidataHeader(lista):
    string = 'http://www.wikidata.org/entity/'
    return [elemento.replace(string, '') for elemento in lista if elemento.startswith(string)]

def delete_property(claims, list_of_properties):
    for property in list_of_properties:
        if property in claims:
            del claims[property]

#reduce_entity: filtra el formato de JSON de Wikidata, eliminando algunas propiedades y simplificando algunas estructuras
#Es recomendable estudiar más a fondo filtrar más información para reducir el tamaño del archivo JSON final de Wikidata
def reduce_entity(entity):
    claims = entity['claims']
    count_order_errors = 0
    # if claims['rank'] == 'deprecated':
    #     return None
    delete_property(claims, ['id', 'references', 'sitelinks', 'labels'])
    for llave in claims:
        valores = claims[llave]
        n = len(valores)
        for i in range(n):
            objeto = valores[i]
            valor = objeto['mainsnak']
            mainsnak = {"datatype":valor["datatype"]}
            if valor['snaktype'] == "value":
                datavalue = reduce_datavalue(valor['datavalue'])
                mainsnak["datavalue"] = datavalue
            new_object = {'mainsnak':mainsnak, 'rank':objeto['rank']}
            #Se eliminan los qualifiers, siempre y cuando no hagan alusión al orden de un autor de una entidad
            #P50 = author, P2093 = string author property
            if llave == 'P50' or llave == 'P2093':
                if "qualifiers" in objeto:
                    #P1545: orden del autor
                    if "P1545" in objeto["qualifiers"]:
                        #Si existe el orden dentro de la propiedad, se añade al objeto
                        try:
                            new_object['order'] = objeto["qualifiers"]["P1545"][0]["datavalue"]["value"] #####
                        except:
                            count_order_errors += 1
                    
            entity['claims'][llave][i] = new_object

    return entity, count_order_errors
    

class WikidataParser():

    def __init__(self):
        #Ubicación del dump de Wikidata
        #self.path = "db/gz/latest-all.json.gz"
        #Carpeta de datos
        self.folder = 'Wikidata_parser/data/'

        #Acceso a rutas de conteos de referencias en todo Wikidata a propiedades de entidades con IDs de DBLP
        publication_path = self.folder + 'query_publication_dblp.csv'
        publication_filter = readCSV(publication_path)
        self.publication_filter = replaceWikidataHeader(publication_filter)

        event_path = self.folder + 'query_event_dblp.csv'
        event_filter = readCSV(event_path)
        self.event_filter = replaceWikidataHeader(event_filter)

        venue_path = self.folder + 'query_venue_dblp.csv'
        venue_filter = readCSV(venue_path)
        self.venue_filter = replaceWikidataHeader(venue_filter)

        discarded_properties_path = self.folder + 'discarded_properties.csv'
        self.other_filters_properties_not = readCSV(discarded_properties_path)[1:]

        self.human = 'Q5'

        occurrence = 'Q1190554' 
        taxon = 'Q16521'
        adm_territorial = 'Q56061'
        arquitectural_estructure = 'Q811979'
        chemical = 'Q11173'
        film = 'Q11424'
        thoroughfare = 'Q83620'
        astronomical = 'Q6999'
        wikimedia_category = 'Q4167836'
        wikimedia_article = 'Q13406463'
        wikimedia_template = 'Q11266439'
        self.other_filters_instances = [occurrence, taxon, adm_territorial, chemical, film, thoroughfare, wikimedia_category, wikimedia_article, wikimedia_template]
        
        self.count_human = 0
        self.count_scholar = 0
        self.count_other = 0

        # carpeta_externa = "D:\Memoria" 

        # self.wikidata_person_file = "wikidata_person_6.json"
        # self.wikidata_scholar_file = "wikidata_scholar_6.json"
        # self.wikidata_else_file = "wikidata_else_6.json"

        # self.wikidata_person_url = os.path.join(carpeta_externa, self.wikidata_person_file)
        # self.wikidata_scholar_url = os.path.join(carpeta_externa, self.wikidata_scholar_file)
        # self.wikidata_else_url = os.path.join(carpeta_externa, self.wikidata_else_file)

    #setters

    def set_path(self, path):
        self.path = path

    def set_wikidata_files(self, wikidata_person_url, wikidata_scholar_url, wikidata_else_url):
        self.wikidata_person_url = wikidata_person_url
        self.wikidata_scholar_url = wikidata_scholar_url
        self.wikidata_else_url = wikidata_else_url

    #filter_name: se filtran los nombres de una entidad
    #Si existe un nombre en inglés, se añade este. De lo contrario, se añaden todos los nombres en todos los idiomas
    def filter_name(self, entity):
        labels = entity['labels']
        if "en" in labels:
            name = {'en':labels['en']}
        else:
            name = labels
        return name

    def filter_aliases(self, entity):
        #return filter_languages(entity, "aliases")
        if 'aliases' in entity:
            aliases = entity['aliases']
            if "en" in aliases:
                alias = {'en':aliases['en']}
            else:
                alias = aliases
            return alias
        else:
            return None
    
    #filter_descriptions: se filtran las descripciones de una entidad
    #Si existe una descripción en inglés, se añade este. De lo contrario, se añaden todas las descripciones en todos los idiomas
    def filter_descriptions(self, entity):
    #return filter_languages(entity, "descriptions")
        try:
            descriptions = entity['descriptions']
            if "en" in descriptions:
                description = {'en':descriptions['en']}
                #description = entity['descriptions']['en']['value']
            else:
                description = descriptions
            return description
        except:
            return None
        
    def filter_id(self, entity, dict):
        dict['claims'] = {}
        claims = entity['claims']        
        for llave in claims:
            valores = claims[llave]
            for objeto in valores:
                valor = objeto['mainsnak']
                datatype = valor['datatype']
                if datatype == "external-id":
                    if llave not in dict['claims']:
                        dict['claims'][llave] = []
                    mainsnak = {"datatype":valor["datatype"]}
                    if valor['snaktype'] == "value":
                        datavalue = reduce_datavalue(valor['datavalue'])
                        mainsnak["datavalue"] = datavalue
                    new_object = {'mainsnak':mainsnak, 'rank':objeto['rank']}
                    # if "qualifiers" in valor:
                    #     new_object['qualifiers':valor['qualifiers']]
                    dict['claims'][llave].append(new_object)

    def filter_scholar(self, instances_list):
        valid = False
        for llave in instances_list:
            if llave in self.other_filters_properties_not:
                return False
            if llave in self.publication_filter or llave in self.event_filter or llave in self.venue_filter:
                valid = True
        return valid

    def filter_instances(self, instances, filtros):
        for llave in instances:
            if llave in filtros:
                return True
        return False
    
    def write_entities(self, file, entity, name, empty):
        if not empty:
            #file.write(",")
            file.write("\n")                   
        entity['name'] = name
        #del entity['labels']
        if 'aliases' in entity:
            entity['aliases'] = self.filter_aliases(entity)
        description = self.filter_descriptions(entity)
        if description:                     
            entity['description'] = description
            del entity['descriptions']
        entity, count_order_error = reduce_entity(entity)
        ujson.dump(entity, file)
        empty = False
        return empty, count_order_error

    def parse_wikidata(self):

        inicio = time.time()

        with gzip.open(self.path, 'rt', encoding='utf-8') as wikidata_dump, open(self.wikidata_person_url, "w") as wikidata_person, open(self.wikidata_scholar_url, "w") as wikidata_scholar, open(self.wikidata_else_url, "w") as wikidata_else:
            
            empty_person = True
            empty_scholar = True
            empty_other = True

            for line in wikidata_dump:
                #ajustar linea para poder ser procesada como objeto JSON
                line = line.strip()

                if line in {"[", "]"}:
                    continue
                if line.endswith(","):
                    line = line[:-1]
                entity = ujson.loads(line)

                id = entity['id']
                name = self.filter_name(entity)
                claims = entity['claims']
                if 'P31' in claims:
                    instances = claims['P31']
                else:
                    continue
                instances_list = []
                for instance in instances:
                    if 'datavalue' in instance['mainsnak']:
                        instance_value = instance['mainsnak']['datavalue']['value']['id']
                        instances_list.append(instance_value)  
                
                #Procesar personas de Wikidata
                if self.human in instances_list:
                    if not empty_person:
                        wikidata_person.write("\n")
                    human_dict = {'id':id, 'name':name}
                    description = self.filter_descriptions(entity)
                    if description:  
                        human_dict['description'] = description
                    human_dict = self.filter_id(entity, human_dict)
                    #human_dict = reduce_entity(human_dict)
                    ujson.dump(human_dict, wikidata_person)
                    empty_person = False
                    self.count_human += 1
                    #break

                                #Procesar scholar_articles o relacionados directos de Wikidata           
                elif self.filter_scholar(instances_list):
                    #print('a')
                    empty_scholar, count_order_error = self.write_entities(wikidata_scholar, entity, name, empty_scholar)
                    self.count_scholar += 1
                    #count_order_errors += count_order_error
                    #break

                #Procesar otras entidades de Wikidata    
                elif (not self.filter_instances(instances_list, self.other_filters_instances)):
                    if (not self.filter_instances(claims, self.other_filters_properties_not)):
                        empty_other, count_order_error = self.write_entities(wikidata_else, entity, name, empty_other)
                        self.count_other += 1
                        #count_order_errors += count_order_error     


        fin = time.time()
        tiempo = fin - inicio
        print("Tiempo de lectura, {} segundos.".format(tiempo))

        print("Número de personas: {}".format(self.count_human))
        print("Número de scholar articles: {}".format(self.count_scholar))
        print("Número de entidades en el archivo 3: {}".format(self.count_other))


if __name__ == "__main__":



    wikidata_parser = WikidataParser()

    #Ajustar rutas del archivo comprimido de Wikidata y los archivos resultantes en formato JSON
    carpeta_externa = "D:\Memoria" 
    path = "db/gz/latest-all.json.gz"
    wikidata_person_file = "wikidata_person.json"
    wikidata_scholar_file = "wikidata_scholar.json"
    wikidata_else_file = "wikidata_else.json"

    wikidata_person_url = os.path.join(carpeta_externa, wikidata_person_file)
    wikidata_scholar_url = os.path.join(carpeta_externa, wikidata_scholar_file)
    wikidata_else_url = os.path.join(carpeta_externa, wikidata_else_file)
    wikidata_parser.set_path(path)
    wikidata_parser.set_wikidata_files(wikidata_person_url, wikidata_scholar_url, wikidata_else_url)

    #Ejecutar preprocesamiento de Wikidata
    wikidata_parser.parse_wikidata()