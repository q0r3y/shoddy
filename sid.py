import sys
import hashlib
import requests
from os import path
from math import ceil
from time import time

def req_chunk(start, end):
    headers = {"Range": "bytes="+str(start)+"-"+str(end)}
    chunk = session.get(web_url, headers=headers)
    return chunk

def get_chunk_indexes(number_of_chunks, file_size):
    chunk_size = ceil(file_size / number_of_chunks)
    return [(start, min(start + chunk_size - 1, file_size - 1)) 
             for start in range(0, file_size, chunk_size)]

def get_num_chunks(file_size):
    megabytes = len(str(int(file_size/1000000)))
    min_chunks = 1**megabytes
    max_chunks = 5**megabytes
    for i in range(max_chunks, min_chunks, -1):
        if file_size % i == 0:
            return i

def print_sha256(file_name):
    sha256_hash = hashlib.sha256()
    with open(file_name,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        print(f'[*] SHA256: {sha256_hash.hexdigest()}')

def progress_bar(current, total, bar_length=20):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current == total else '\r'
    print(f'[*] Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)

def is_download_complete(file_name, file_size):
    drive_file_size = path.getsize(file_name)
    return drive_file_size == file_size

def partial_file_exists(file_name):
    return path.exists(file_name)

def get_partial_file_size(file_name):
    return path.getsize(file_name)

try:
    progress = 0
    web_url = sys.argv[1]
    file_name = web_url.split('/')[-1]
    file_size = int(requests.head(web_url).headers['Content-Length'])
    print(f'[+] Web request found file: {file_name}')
    print(f'[+] File size: {file_size/1000000} MB')
    num_chunks = get_num_chunks(file_size)

    print(f'[+] Number of chunks set to: {num_chunks}')

    chunks_indexes = get_chunk_indexes(num_chunks, file_size)

    print(f'Num_chunks: {num_chunks}')
    print(f'chunks_indexes: {chunks_indexes}')
    
    if (partial_file_exists(file_name)):
        print('Found file')
        last_chunk = get_partial_file_size(file_name)
        print(f'last_chunk: {last_chunk}')
        index = 0
        for i in chunks_indexes:
            for j in i:
                if j == last_chunk:
                    progress = index
                    chunks_indexes = chunks_indexes[index:]
                    print(f'[*] Partial File Found. Resuming Progress at chunk: {index} / {num_chunks}')
                    break
            index += 1

    session = requests.Session()
    with open(file_name, 'ab') as file:
        start_time = time()
        progress_bar(progress, num_chunks)
        for i,(start, end) in enumerate(chunks_indexes):
            file.write(req_chunk(start, end).content)
            progress += 1
            progress_bar(progress, num_chunks)
        end_time = time()
    

    if is_download_complete(file_name, file_size):
        seconds = 0
        print(f'[+] Download completed in: {end_time - start_time} seconds')
        print_sha256(file_name)
    

except IndexError:
    print('[-] Missing argument')
except KeyError:
    print('[-] Missing header: Content-Length')
except requests.exceptions.MissingSchema:
    print('[-] Argument is not a valid URL')
except requests.exceptions.ConnectionError:
    print('[-] Connection lost')
    print(f'[*] Chunks completed: {progress}')
except KeyboardInterrupt:
    print('\n[-] Script execution cancelled')
    print(f'[*] Chunks completed: {progress} / {num_chunks}')
# except:
#     print("[-] An unknown error has occured")
