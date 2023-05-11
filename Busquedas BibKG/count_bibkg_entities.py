import json 
import time

bibkg_p1_url = "bibkg_part1.json"
bibkg_p2_url = "bibkg_part2.json"
bibkg_p3_url = "bibkg_part3.json"
bibkg_p4_url = "bibkg_part4.json"

bibkg_url = "bibkg.json"


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

inicio = time.time()
with open(bibkg_url, 'r') as bibkg:
    for linea in bibkg:
        entity = json.loads(linea)
        id = entity['id']
        if id == 'a_Aidan_Hogan':
            print(entity)
        for key in entity:
            if "\"" in key:
                count_comillas += 1
            if " " in key:
                count_espacios += 1
            #break
        if "author_of" in entity:
            c_author += 1
        print(entity)
        if c1 > 10:
            break
        c1 += 1
fin = time.time()
print(c_author)
print(c1)
print(count_comillas)
print(count_espacios)
print("Tiempo de ejecución: {} segundos".format(fin - inicio))
#         if 'has_author' in entity:
#             count_has_author += 1
#         if 'url' in entity:
#             count_url += 1
#         if 'serie' in entity:
#             count_serie += 1
#         if 'in_proceedings' in entity:
#             count_in_proceedings += 1
#         if 'cites' in entity:
#             count_cites += 1
#         if not "type" in entity:
#             count_none += 1
#         else:
#             type = entity['type']
#             if type == "Person":
#                 count_person += 1
#             elif type == "Article":
#                 count_article += 1
#             elif type == "Journal":
#                 count_journal += 1
#             elif type == "Inproceedings":
#                 count_inproceedings += 1
#             elif type == "Field":
#                 count_field += 1
#         count_entities += 1
#         # for key in entity:
#         #     if "\"" in key:
#         #         count_errors += 1
#         # if 'author_of' in entity:
#         #     print(entity)
#         #     break

# print("Total entities: {}".format(count_entities))
# print("Total errors: {}".format(count_errors))
# print(count_none)
# print("Total person: {}".format(count_person))
# print("Total articles: {}".format(count_article))
# print("Total journals: {}".format(count_journal))
# print("Total inproceedings: {}".format(count_inproceedings))
# print("Total fields: {}".format(count_field))

# print(count_has_author)
# print(count_url)
# print(count_serie)
# print(count_in_proceedings)

# bibkg_url = 'milleDB.dump'
# with open(bibkg_url, encoding="utf8") as bibkg:
#     for linea in bibkg:
#         if "Netflix" in linea and "a_Hal_Tily" in linea:
#             print(linea)



