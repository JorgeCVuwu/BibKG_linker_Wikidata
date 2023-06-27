import json
import gzip

count = 0
obj_list = []
with gzip.open('latest-all.json.gz', 'rt', encoding='utf-8') as f:
    json_parser = json.JSONDecoder()
    buffer_size = 1024  # Tamaño del búfer en bytes
    buffer = ""
    while True:
        block = f.read(buffer_size)
        if not block:
            # Fin del archivo
            break
        buffer += block
        try:
            while buffer.strip():
                obj, idx = json_parser.raw_decode(buffer)
                buffer = buffer[idx:].lstrip()
                # Utiliza el objeto obj como lo necesites
                print(obj)
                obj_list.append(obj)
        except ValueError:
            # No hay suficiente información para parsear, continúa leyendo
            pass
        if len(buffer) > 1000000:
            print(buffer)
            print(obj_list)
            break
        