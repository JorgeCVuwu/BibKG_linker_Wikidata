import gzip
import json
import time
import ujson
import os

def filter_name(entity):
    if "en" in entity['labels']:
        name = entity['labels']['en']['value']
    else:
        name = entity['labels']
    return name

def filter_descriptions(entity):
    try:
        if "en" in entity['descriptions']:
            description = entity['descriptions']['en']['value']
        else:
            description = entity['descriptions']
        return description
    except:
        return None

def filter_id(entity, dict):
    claims = entity['claims']        
    for llave in claims:
        valores = claims[llave]
        # if llave == 'P735': #given name
        #     human_dict['P735'] = valores
        # if llave == 'P734': #family name
        #     human_dict['P734'] = valores
        for valor in valores:
            datatype = valor['mainsnak']['datatype']
            if datatype == "external-id":
                dict[llave] = valores
                break
    return dict

def filter_instances(instances, filtros):
    for llave in instances:
        if llave in filtros:
            return True
    return False

def write_entities(file, entity, empty):
    if not empty:
        file.write(",")
        file.write("\n")                   
    entity['name'] = name
    del entity['labels']
    try:
        del entity['sitelinks']
    except:
        pass
    try:
        del entity['aliases']
    except:
        pass
    description = filter_descriptions(entity)
    if description:                     
        entity['description'] = description
        del entity['descriptions']
    ujson.dump(entity, file)
    empty = False
    return empty
                        

path = "latest-all.json.gz"
c = 0
len_wikidata = 100000000

human = 'Q5'

scholar_article = 'Q13442814'
chapter = 'Q1980247'
written_work = 'Q47461344'
conference_paper = 'Q23927052'
scientific_conference_paper = 'Q10885494'
scientific_conference_series = 'Q47258130'
scientific_journal = 'Q5633421'
publication = 'Q732577'
proceedings = 'Q1143604'
academic_conference = 'Q2020153'
academic_journal = ''

publication_filter = [scholar_article, chapter, written_work, scientific_conference_paper, conference_paper, scientific_journal, scientific_conference_series, publication, proceedings, academic_conference]

author = 'P50'
author_name_string = 'P2093'

PubMed_ID = 'P698'
apparent_magnitude = 'P1215'
PMCID = 'P932'
astronomical_filter = 'P1227'
SIMBAD_ID = 'P3083'

other_filters_properties = [author]

other_filters_properties_not = [PubMed_ID, PMCID, apparent_magnitude, astronomical_filter, SIMBAD_ID]


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

#limit = 100000
inicio = time.time()


carpeta_externa = "D:\Memoria" 

wikidata_person_file = "wikidata_person.json"
wikidata_scholar_file = "wikidata_scholar.json"
wikidata_else_file = "wikidata_else.json"

wikidata_person_url = os.path.join(carpeta_externa, wikidata_person_file)
wikidata_scholar_url = os.path.join(carpeta_externa, wikidata_scholar_file)
wikidata_else_url = os.path.join(carpeta_externa, wikidata_else_file)

with gzip.open(path, 'rt', encoding='utf-8') as file, open(wikidata_person_url, "w") as wikidata_person, open(wikidata_scholar_url, "w") as wikidata_scholar, open(wikidata_else_url, "w") as wikidata_else:
    wikidata_person.write("[")
    wikidata_scholar.write("[")
    wikidata_else.write("[")
    empty_person = True
    empty_scholar = True
    empty_other = True
    for line in file:
        line = line.strip()

        if line in {"[", "]"}:
            continue
        if line.endswith(","):
            line = line[:-1]
        entity = ujson.loads(line)

        # do your processing here
        #print(str(entity))
        if entity:# and c < limit:
            try:
                add_person = False
                add_scholar = False
                add_else = False
                id = entity['id']
                name = filter_name(entity)
                claims = entity['claims']
                instances = claims['P31']
                instances_list = []
                for instance in instances:
                    instance_value = instance['mainsnak']['datavalue']['value']['id']
                    instances_list.append(instance_value)              

                #Procesar personas de Wikidata
                if human in instances_list:
                    if not empty_person:
                        wikidata_person.write(",")
                        wikidata_person.write("\n")
                    human_dict = {'id':id, 'name':name}
                    description = filter_descriptions(entity)
                    if description:  
                        human_dict['description'] = description
                    human_dict = filter_id(entity, human_dict)
                    ujson.dump(human_dict, wikidata_person)
                    empty_person = False
                    count_human += 1
                    #break     

                #Procesar scholar_articles o relacionados directos de Wikidata           
                elif filter_instances(instances_list, publication_filter):
                    empty_scholar = write_entities(wikidata_scholar, entity, empty_scholar)
                    count_scholar += 1
                    #break

                #Procesar otras entidades de Wikidata    
                elif (filter_instances(claims, other_filters_properties)) and (not filter_instances(instances_list, other_filters_instances)):
                    if (not filter_instances(claims, other_filters_properties_not)):
                        empty_other = write_entities(wikidata_else, entity, empty_other)
                        count_other += 1

            except Exception as e:
                # print(e)
                # print(f"Ocurrió un error de tipo {type(e).__name__}")
                pass
        c += 1
        #if c >= limit:
        #    break
    wikidata_person.write(']')
    wikidata_scholar.write(']')
    wikidata_else.write(']')

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

# print(id)
# print(name)
# print(ins)