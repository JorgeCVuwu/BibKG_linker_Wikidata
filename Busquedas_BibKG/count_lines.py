import time
 
start = time.time()
count = 0
#(count_person, count_article, count_field, count_journal, count_wikidata)
counts = [0,0,0,0,0,0]
total = 144779468
n = len(counts)
with open("milleDB.dump", encoding="utf8") as file:
    for line in file:
       #print(line)
       if "a_Aidan_Hogan" in line and "Universidad de Chile" in line:
           print(line)
    #    line_counts = tuple(map(line.count, (":Person", ":Article", ":Field", ":Journal", "wikidata:", "author_of")))
    #    for i in range(n):
    #        counts[i] += line_counts[i]
    #    count = count + 1
    #    if count < 100:
    #         print(line)
    #    if count > 100:
    #        break
       #print("\rporcentaje: " + str(round((count/total)*100, 2)) + "%", end='')

end =  time.time()
print("Execution time in seconds: ",(end-start))
print("No of lines printed: ",count)
print("Different counts: ", counts)

#lines: 144779468
#48255 referencias a Wikidata en total
#48