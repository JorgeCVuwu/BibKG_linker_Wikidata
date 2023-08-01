import gzip
import json
import time
import ujson

path = "latest-all.json.gz"
c = 0
len_wikidata = 100000000
#occurrence, taxon, administrative territorial entity, chemical conpound
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

instance_filter = [occurrence, taxon, adm_territorial, chemical, film, thoroughfare, wikimedia_category, wikimedia_article, wikimedia_template]

human = 'Q5'
scholar_article = 'Q13442814'

entity_list = []
name_list = []
publication_list = []
person_objets = []

count_human = 0

limit = 100
inicio = time.time()
with gzip.open(path, 'rt', encoding='utf-8') as file, open("wikidata_person_washington_original.json", "w") as wikidata_person:
    for line in file:
        line = line.strip()

        if line in {"[", "]"}:
            continue
        if line.endswith(","):
            line = line[:-1]
        entity = ujson.loads(line)

        # do your processing here
        #print(str(entity))
        if entity and c < limit:
            try:
                add = True
                id = entity['id']
                if "en" in entity['labels']:
                    name = entity['labels']['en']['value']
                    entity['name'] = name
                    del entity['labels']
                else:
                    name = entity['labels'][0]
                # entity.pop('labels')
                # entity.pop('descriptions')
                # entity.pop('aliases')
                instances = entity['claims']['P31']
                instances_list = []
                for instance in instances:
                    instance_value = instance['mainsnak']['datavalue']['value']['id']
                    instances_list.append(instance_value)
                for i in instances_list:
                    if i in instance_filter:
                        add = False
                        break
                if scholar_article in instances_list:
                    publication_list.append(name)
                if human not in instances_list:
                    add = False
                else:
                    #person_objets.append(entity)
                    count_human += 1
                    ujson.dump(entity, wikidata_person)
                    wikidata_person.write("\n")
                    break
                if add:
                    entity_list.append(id)
                    #name_list.append(name)

                    
            #print(str(entity)[:1500])
            #break
            except:
                #print(e)
                # print(c)
                # print(id)
                pass
        c += 1
        if c >= limit:
            break

fin = time.time()
tiempo = fin - inicio
print("Tiempo de lectura, {} segundos.".format(tiempo))
print("Promedio: {} segundos.".format(tiempo/c))

#with open("wikidata_person.json", "w") as f:
#    ujson.dump(person_objets, f)

print("c: ", c)
horas_estimadas = (tiempo/c)*len_wikidata/3600
print("Tiempo estimado de lectura y escritura para todo el dump: {} horas".format(horas_estimadas))


#print(name_list)

for v in entity['claims']['P535']:
    print(v)
    print("AAAAAAAAAAAAAAA")
# print(id)
# print(name)
# print(ins)