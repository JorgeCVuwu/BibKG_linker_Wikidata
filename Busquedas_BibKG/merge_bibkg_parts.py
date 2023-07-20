import json

folder = "db/JSON/"

bibkg_p1_url = folder + "bibkg10.json"
bibkg_p2_url = folder + "bibkg20.json"

parts_list = [bibkg_p1_url, bibkg_p2_url]

new_bibkg_url = folder + "bibkg.json"

def merge_bibkg(parts_list, new_bibkg_url):
    c1 = 0
    c2 = 0
    bibkg_p1_url, bibkg_p2_url = parts_list[0], parts_list[1]
    entity_dict = {}
    repeated_dict = {}
    repeated_objects = {}

    repeated_counts = {}

    with open(bibkg_p1_url, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if id not in entity_dict:
                entity_dict[id] = 0
            entity_dict[id] += 1
            #print(entity)
            c1 += 1

    with open(bibkg_p2_url, 'r') as bibkg:
        for linea in bibkg:
            entity = json.loads(linea)
            id = entity['id']
            if id not in entity_dict:
                entity_dict[id] = 0
            entity_dict[id] += 1
            #print(entity)
            c2 += 1

    c_repeated = 0

    for key, valor in entity_dict.items():
        if valor > 1:
            repeated_dict[key] = valor
            c_repeated += 1

    print(c1)
    print(c2)
    print(c_repeated)

    print("Total: {}".format((c1 + c2) - c_repeated))

    with open(new_bibkg_url, 'w') as bibkg, open(bibkg_p1_url, 'r') as p1, open(bibkg_p2_url, 'r') as p2:
        for linea in p1:
            entity = json.loads(linea)
            if 'author_of' in entity:
                del entity['author_of']
            id = entity['id']
            if id not in repeated_dict:
                json.dump(entity, bibkg)
                bibkg.write('\n')
            else:
                if id not in repeated_objects:
                    repeated_objects[id] = entity
                else:
                    repeated_object = repeated_objects[id]
                    for key, value in entity.items():
                        if key in repeated_object and key != "id" and type(repeated_object[key]) == list:
                            for elemento in value:
                                if elemento not in repeated_object[key]:
                                    repeated_objects[id][key].append(elemento)
                            if key not in repeated_counts:
                                repeated_counts[key] = 0
                            repeated_counts[key] += 1
                        else:
                            repeated_objects[id][key] = value

        for linea in p2:
            entity = json.loads(linea)
            if 'author_of' in entity:
                del entity['author_of']
            id = entity['id']
            if id not in repeated_dict:
                json.dump(entity, bibkg)
                bibkg.write('\n')
            else:
                if id not in repeated_objects:
                    repeated_objects[id] = entity
                else:
                    repeated_object = repeated_objects[id]
                    for key, value in entity.items():
                        if key in repeated_object and key != "id" and type(repeated_object[key]) == list:
                            for elemento in value:
                                if elemento not in repeated_object[key]:
                                    repeated_objects[id][key].append(elemento)
                            if key not in repeated_counts:
                                repeated_counts[key] = 0
                            repeated_counts[key] += 1
                        else:
                            repeated_objects[id][key] = value


    print(repeated_counts)

    with open(new_bibkg_url, 'a') as bibkg:
        for key, value in repeated_objects.items():
            json.dump(value, bibkg)
            bibkg.write('\n')


merge_bibkg(parts_list, new_bibkg_url)