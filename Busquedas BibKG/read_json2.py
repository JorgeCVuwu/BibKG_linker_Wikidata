import sys
import time

inicio = time.time()
objetos = sys.argv[1]
fin = time.time()

print("Tiempo de ejecución de la obtención de la variable: " + str(fin - inicio) + " segundos")

for objeto in objetos:
    try:
        pass
    except Exception as e:
        break