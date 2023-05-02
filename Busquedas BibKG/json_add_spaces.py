import json

# Ruta del archivo JSON original
archivo_origen = "bibkg_2.json"

# Ruta del archivo JSON con espacios entre objetos
archivo_destino = "bibkg.json"

with open(archivo_origen, "r") as f_origen, open(archivo_destino, "w") as f_destino:
    # Lee cada línea del archivo original
    for linea in f_origen:
        # Convierte la línea en un objeto JSON
        objeto = json.loads(linea)
        # Convierte el objeto JSON en una cadena con espacios
        objeto_str = json.dumps(objeto) + "\n"
        # Escribe la cadena en el archivo de destino
        f_destino.write(objeto_str)