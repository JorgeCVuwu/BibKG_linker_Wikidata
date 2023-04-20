estudiantes = [
    {'nombre': 'Juan', 'apellido': 'Pérez', 'edad': 20},
    {'nombre': 'María', 'apellido': 'González', 'edad': 19},
    {'nombre': 'Pedro', 'apellido': 'García', 'edad': 21}
]

# Abre un archivo en modo escritura
with open('estudiantes.tsv', 'w') as archivo:
    # Escribe la cabecera del archivo
    archivo.write('Nombre\tApellido\tEdad\n')
    
    # Escribe los datos de cada estudiante en el archivo
    for estudiante in estudiantes:
        linea = '\t'.join([estudiante['nombre'], estudiante['apellido'], str(estudiante['edad'])])
        archivo.write(linea + '\n')