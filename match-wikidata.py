from SPARQLWrapper import SPARQLWrapper, JSON
import wikidata
from wikidata.client import Client
import time

inicio = time.time()
for i in range(10000):
    if (i - 1)%10 == 0:
        inicio = time.time()
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""

    SELECT ?x 
    {?x wdt:P50 wd:Q51366847}

    """)

    # values = []
    results = sparql.queryAndConvert()
    # for r in results["results"]["bindings"]:
    #     value = r['x']['value'].replace("http://www.wikidata.org/entity/","")
    #     values.append(value)
    if i%10 == 0:
        fin = time.time()
        print(i)
        print("Tiempo promedio: " + str((fin - inicio)))
        print("Tiempo promedio: " + str((fin - inicio)/10))
#print(values)




# client = Client()
# entity = client.get("Q51366847", load=True)
# article = client.get("Q30490827", load=True)
# DBLP_key = client.get('P356')
# print(entity)
# instance_of = client.get('P31')
# aidan_instance = entity[instance_of]
# print(aidan_instance)
# print(article)
# key = article[DBLP_key]
# print(key)