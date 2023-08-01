import gzip
import zlib
import os

archivo_gz = "db/gz/latest-all.json.gz"


# Obtener el tamaño del archivo comprimido en bytes
tamano_comprimido = os.path.getsize(archivo_gz)

# Leer solo los primeros 10 bytes del archivo comprimido
with open(archivo_gz, "rb") as f:
    encabezado_gzip = f.read(10)

# Obtener el tamaño descomprimido usando la información del encabezado del gzip
tamano_descomprimido = zlib.decompress(encabezado_gzip[::-1] + b'\x00\x00\x00\x00', 15).size

print(f"Tamaño comprimido: {tamano_comprimido} bytes.")
print(f"Tamaño descomprimido estimado: {tamano_descomprimido} bytes.")