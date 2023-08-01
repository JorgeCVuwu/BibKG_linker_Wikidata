import bz2
import json
import multiprocessing
import time

def process_chunk(chunk):
    for line in chunk:
        line = line.decode().strip()

        if line in {"[", "]"}:
            continue
        if line.endswith(","):
            line = line[:-1]
        entity = json.loads(line)

        if entity and c < 1500:
            #try:
            id = entity['id']
            name = entity['labels']['en']['value']
            if 'P31' in entity['claims']:
                instances = entity['claims']['P31']
                ins = []
                for instance in instances:
                    code = instance['mainsnak']['datavalue']['value']['id']
                    ins.append(code)
            #except Exception as e:
            #    pass

if __name__ == '__main__':
    path = "latest-all.json.bz2"
    chunk_size = 100000  # tamaño de cada trozo
    c = 0
    inicio = time.time()
    with bz2.BZ2File(path) as file:
        pool = multiprocessing.Pool(processes=4) # especificar el número de procesos
        while True:
            chunk = file.readlines(chunk_size)
            if not chunk:
                break
            pool.apply_async(process_chunk, args=(chunk,))
            c += len(chunk)
            if c >= 1500:
                break
        pool.close()
        pool.join()
    fin = time.time()
    print(f"Tiempo total: {fin-inicio}")