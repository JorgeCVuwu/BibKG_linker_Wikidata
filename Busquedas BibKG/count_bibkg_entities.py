import json 
import time

dblp_dict = {}


def process_dblp_url(entity, dblp_dict):
    #print(url)
    url = entity[':url'][0]['value']
    split = url.split('/')
    if split[0] != 'db':
        return False
    url1 = ''
    n = len(split) - 1
    for i in range(1, n):
        url1 += split[i] + '/'
    url_last = split[-1]
    if '#' in url_last:
        url_name =url_last.split('#')[1]
    else:
        url_name = url_last.replace(".html", "")
    dblp_id = url1 + url_name
    dblp_dict[dblp_id] = id


folder = "db/JSON/"

bibkg_p1_url = "bibkg_part1.json"
bibkg_p2_url = "bibkg_part2.json"
bibkg_p3_url = "bibkg_part3.json"
bibkg_p4_url = "bibkg_part4.json"

bibkg_url = folder + "bibkg linked by id.json"


count_errors = 0
count_entities = 0
count_none = 0
count_person = 0
count_article = 0
count_journal = 0
count_inproceedings = 0
count_field = 0
count_has_author = 0
count_url = 0
count_serie = 0
count_in_proceedings = 0
count_cites = 0

c1 = 0
c2 = 0
c_author = 0
count_comillas = 0
count_espacios = 0
entity_dict = {}
count_wikidata = 0

count_url = 0
count_url_dblp = 0

type_count_dict = {}

inicio = time.time()
with open(bibkg_url, 'r') as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        if 'type' in entity:
            type = entity['type']
            id = entity['id']
            if 'has_author' in entity:
                for author in entity['has_author']:
                    if 'a_Aidan_Hogan' in author['value']:
                        if 'wikidata' in entity:
                            print("wikidata: {}".format(entity['wikidata']))
                            if 'ee' in entity:
                                print("ee: {}".format(entity['ee']))
        c1 += 1
fin = time.time()
print(count_url)
print(count_url_dblp)
print(type_count_dict)