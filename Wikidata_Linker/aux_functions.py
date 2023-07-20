import re

def is_number(string):
    patron = r'^\d+$'
    if re.match(patron, string):
        return True
    else:
        return False

def process_names(name):
    name = str(name)
    split = name.split()
    resultado = name
    if len(split) == 3:
        if (len(split[1]) == 2 and "." in split[1]) or len(split[1]) == 1:
            resultado = split[0] + ' ' + split[2]
        elif is_number(split[2]):
            resultado = split[0] + ' ' + split[1]
        # else:
        #     print(name)
    return resultado.replace(".", "").lower()

def process_author_id(id):
    if id[0:2] == "a_":
        return id[2:].replace("_", " ")
    
def get_year(date):
    year = date[1:5]
    return year

