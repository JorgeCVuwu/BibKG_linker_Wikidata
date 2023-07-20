import pandas as pd

def contar_valores_csv(nombre_archivo):
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(nombre_archivo)
    
    # Contar la cantidad de valores en cada columna
    conteo_valores = df.count()
    
    return conteo_valores

# Nombre del archivo CSV
archivo_csv = 'data/wikidata_linker/linked-entities-4.csv'
#archivo_csv = 'data/wikidata_linker/id-links-corr.csv'


# Obtener el conteo de valores en cada columna
conteo = contar_valores_csv(archivo_csv)

# Imprimir el resultado
print(conteo)