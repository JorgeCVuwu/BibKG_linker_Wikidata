import gzip
import json
import time
import ujson
import os
import csv

def filter_name(entity):
    labels = entity['labels']
    if "en" in labels:
        name = {'en':labels['en']}
        #name = entity['labels']['en']['value']
    else:
        name = labels
    return name

def filter_descriptions(entity):
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
    
def filter_aliases(entity):
    #return filter_languages(entity, "aliases")
    try:
        aliases = entity['aliases']
        if "en" in aliases:
            alias = {'en':aliases['en']}
        else:
            alias = aliases
        return alias
    except:
        return None
    
def filter_languages(entity, key):
    try:
        aliases = entity[key]
        if "en" in aliases:
            alias = {'en':aliases['en']}
        else:
            alias = aliases
        return alias
    except:
        return None

def filter_id(entity, dict):
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
                
    return dict

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

def reduce_entity(entity):
    claims = entity['claims']
    count_order_errors = 0
    # if claims['rank'] == 'deprecated':
    #     return None
    try:
        del entity['claims']['id']
    except:
        pass
    try:
        del entity['claims']['references']
    except:
        pass
    for llave in claims:
        valores = claims[llave]
        n = len(valores)
        #print(valores)
        for i in range(n):
            objeto = valores[i]
            # if objeto['rank'] == 'deprecated':
            #     del entity['claims'][llave][i]
            #     del_count += 1
            #else:
            valor = objeto['mainsnak']
            mainsnak = {"datatype":valor["datatype"]}
            if valor['snaktype'] == "value":
                datavalue = reduce_datavalue(valor['datavalue'])
                mainsnak["datavalue"] = datavalue
            new_object = {'mainsnak':mainsnak, 'rank':objeto['rank']}
            if llave == 'P50' or llave == 'P2093':
                if "qualifiers" in objeto:
                    #P1545: orden del autor
                    if "P1545" in objeto["qualifiers"]:
                        try:
                            new_object['order'] = objeto["qualifiers"]["P1545"][0]["datavalue"]["value"]
                        except:
                            count_order_errors += 1
                            #print(id)
                            #pass
                    
            # if "qualifiers" in objeto:
            #     new_object['qualifiers':objeto['qualifiers']]
            entity['claims'][llave][i] = new_object

    return entity, count_order_errors

def filter_instances(instances, filtros):
    for llave in instances:
        if llave in filtros:
            return True
    return False

def write_entities(file, entity, name, empty):
    if not empty:
        #file.write(",")
        file.write("\n")                   
    entity['name'] = name
    del entity['labels']
    try:
        del entity['sitelinks']
    except:
        pass
    try:
        entity['aliases'] = filter_aliases(entity)
    except:
        pass
    description = filter_descriptions(entity)
    if description:                     
        entity['description'] = description
        del entity['descriptions']
    entity, count_order_error = reduce_entity(entity)
    ujson.dump(entity, file)
    empty = False
    return empty, count_order_error

def replaceWikidataHeader(lista):
    string = 'http://www.wikidata.org/entity/'
    return [elemento.replace(string, '') for elemento in lista if elemento.startswith(string)]

def readCSV(path):
    columna = 0
    filter_list = []
    with open(path, mode='r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            elemento = fila[columna]
            filter_list.append(elemento)

    return filter_list

def filter_scholar(instances_list, publication_filter, event_filter, venue_filter, other_filters_properties_not):
    valid = False
    for llave in instances_list:
        if llave in other_filters_properties_not:
            return False
        if llave in publication_filter or llave in event_filter or llave in venue_filter:
            valid = True
    return valid

                        

path = "db/gz/latest-all.json.gz"
c = 0
len_wikidata = 100000000

folder = 'Wikidata parser/data/'

publication_path = folder + 'query_publication_dblp.csv'
publication_filter = readCSV(publication_path)
publication_filter = replaceWikidataHeader(publication_filter)

event_path = folder + 'query_event_dblp.csv'
event_filter = readCSV(event_path)
event_filter = replaceWikidataHeader(event_filter)

venue_path = folder + 'query_venue_dblp.csv'
venue_filter = readCSV(venue_path)
venue_filter = replaceWikidataHeader(venue_filter)

human = 'Q5'
author_path = folder + 'query_author_dblp.csv'
author_filter = [human]

discarded_properties_path = folder + 'discarded_properties.csv'
other_filters_properties_not = readCSV(discarded_properties_path)[1:]

# Imprime los datos leídos del archivo CSV

author = 'P50'
author_name_string = 'P2093'

other_filters_properties = [author]

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

other_filters_instances = [occurrence, taxon, adm_territorial, chemical, film, thoroughfare, wikimedia_category, wikimedia_article, wikimedia_template]

count_human = 0
count_scholar = 0
count_other = 0

limit = False
inicio = time.time()


carpeta_externa = "D:\Memoria" 

wikidata_person_file = "wikidata_person_4.json"
wikidata_scholar_file = "wikidata_scholar_4.json"
wikidata_else_file = "wikidata_else_4.json"

wikidata_person_url = os.path.join(carpeta_externa, wikidata_person_file)
wikidata_scholar_url = os.path.join(carpeta_externa, wikidata_scholar_file)
wikidata_else_url = os.path.join(carpeta_externa, wikidata_else_file)

# wikidata_person_url = wikidata_person_file
# wikidata_scholar_url = wikidata_scholar_file
# wikidata_else_url = wikidata_else_file

with gzip.open(path, 'rt', encoding='utf-8') as file, open(wikidata_person_url, "w") as wikidata_person, open(wikidata_scholar_url, "w") as wikidata_scholar, open(wikidata_else_url, "w") as wikidata_else:
    # wikidata_person.write("[")
    # wikidata_scholar.write("[")
    # wikidata_else.write("[")
    empty_person = True
    empty_scholar = True
    empty_other = True
    count_order_errors = 0
    for line in file:
        line = line.strip()

        if line in {"[", "]"}:
            continue
        if line.endswith(","):
            line = line[:-1]
        entity = ujson.loads(line)
        try:
            # do your processing here
            #print(str(entity))
            if entity:
                add_person = False
                add_scholar = False
                add_else = False
                id = entity['id']
                name = filter_name(entity)
                claims = entity['claims']
                try:
                    instances = claims['P31']
                except:
                    continue
                instances_list = []
                for instance in instances:
                    instance_value = instance['mainsnak']['datavalue']['value']['id']
                    instances_list.append(instance_value)              

                #Procesar personas de Wikidata
                if human in instances_list:
                    if not empty_person:
                        #wikidata_person.write(",")
                        wikidata_person.write("\n")
                    human_dict = {'id':id, 'name':name}
                    description = filter_descriptions(entity)
                    if description:  
                        human_dict['description'] = description
                    human_dict = filter_id(entity, human_dict)
                    #human_dict = reduce_entity(human_dict)
                    ujson.dump(human_dict, wikidata_person)
                    empty_person = False
                    count_human += 1
                    #break     

                #Procesar scholar_articles o relacionados directos de Wikidata           
                elif filter_scholar(instances_list, publication_filter, event_filter, venue_filter, other_filters_properties_not):
                    #print('a')
                    empty_scholar, count_order_error = write_entities(wikidata_scholar, entity, name, empty_scholar)
                    count_scholar += 1
                    count_order_errors += count_order_error
                    #break

                #Procesar otras entidades de Wikidata    
                elif (not filter_instances(instances_list, other_filters_instances)):
                    if (not filter_instances(claims, other_filters_properties_not)):
                        empty_other, count_order_error = write_entities(wikidata_else, entity, name, empty_other)
                        count_other += 1
                        count_order_errors += count_order_error
        except:
            pass
        c += 1
        if limit:
            if c >= limit:
                break
        if c%10000000 == 0:
            print(c/100000000)
    # wikidata_person.write(']')
    # wikidata_scholar.write(']')
    # wikidata_else.write(']')

fin = time.time()
tiempo = fin - inicio
print("Tiempo de lectura, {} segundos.".format(tiempo))
print("Promedio: {} segundos.".format(tiempo/c))

#with open("wikidata_person.json", "w") as f:
#    ujson.dump(person_objets, f)

print("c: ", c)
horas_estimadas = (tiempo/c)*len_wikidata/3600
print("Tiempo estimado de lectura y escritura para todo el dump: {} horas".format(horas_estimadas))


print("Número de personas: {}".format(count_human))
print("Número de scholar articles: {}".format(count_scholar))
print("Número de entidades en el archivo 3: {}".format(count_other))

print("Número de errores de orden: {}".format(count_order_errors))



# print(id)
# print(name)
# print(ins)

data = [
    ['time_seconds', 'time_hours', 'total_entities', 'person_entities', 'scholarly_entities', 'other_entities'],
    [tiempo, tiempo/3600, c, count_human, count_scholar, count_other]
]
metadata_path = folder + 'wikidata-parser-metadata-3.csv'
with open(metadata_path, mode='w', newline='') as archivo_csv:
    
    # Crea el objeto de escritura de CSV
    writer = csv.writer(archivo_csv)
    
    # Escriba los datos en el archivo CSV
    for fila in data:
        writer.writerow(fila)

print("Metadatos guardados.")