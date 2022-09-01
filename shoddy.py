import sys
import hashlib
import requests
from math import ceil
from time import time
from os import path, rename, remove

class Download:

    def __init__(self, url):
        self.progress = 0
        self.url = url
        self.file_name = url.split('/')[-1]
        self.file_name_part = self.file_name + '.PART'
        self.file_size = self.get_file_size()
        self.file_size_mb = self.file_size / 1000000
        self.set_num_chunks()
        self.set_chunk_indexes()

    def get_file_size(self):
        return int(requests.head(self.url).headers['Content-Length'])

    def set_num_chunks(self):
        digits = len(str(int(self.file_size_mb)))
        min_chunks = 1**digits
        max_chunks = 5**digits
        for i in range(max_chunks, min_chunks, -1):
            if self.file_size % i == 0:
                self.num_of_chunks = i
                break

    def set_chunk_indexes(self):
        chunk_size = ceil(self.file_size / self.num_of_chunks)
        self.chunk_indexes = [(start, min(start + chunk_size - 1, self.file_size - 1)) 
            for start in range(0, self.file_size, chunk_size)]

    def req_chunk(self, start, end):
        headers = {"Range": "bytes="+str(start)+"-"+str(end)}
        chunk = dl.session.get(self.url, headers=headers)
        return chunk

    def begin_download(self, file_path):
        self.progress_bar(self.progress, self.num_of_chunks)
        for i,(start, end) in enumerate(self.chunk_indexes):
            file_path.write(self.req_chunk(start, end).content)
            self.progress += 1
            self.progress_bar(self.progress, self.num_of_chunks)

    def progress_bar(self, current, total, bar_length=20):
        fraction = current / total
        arrow = int(fraction * bar_length - 1) * '-' + '>'
        padding = int(bar_length - len(arrow)) * ' '
        ending = '\n' if current == total else '\r'
        print(f'[*] Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)


def print_sha256(file_name):
    sha256_hash = hashlib.sha256()
    with open(file_name,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        print(f'[*] SHA256: {sha256_hash.hexdigest()}')

def set_download_progress(dl):
    existing_chunk_pos = path.getsize(dl.file_name_part)
    print(existing_chunk_pos)
    index = 0
    for chunk in dl.chunk_indexes:
        if (chunk[0] == existing_chunk_pos) or (chunk[1] == existing_chunk_pos):
            dl.progress = index
            dl.chunk_indexes = dl.chunk_indexes[index:]
            break
        # File exists but didn't leave off at a known chunk position
        elif (existing_chunk_pos > chunk[0]) and (existing_chunk_pos < chunk[1]):
            print('Existing position is between chunk beginning and end')
            print(f'{chunk[0]} {existing_chunk_pos} {chunk[1]}')
            rename(dl.file_name_part, f'{dl.file_name_part}.temp')
            with open(f'{dl.file_name_part}.temp', 'rb') as i_f, open(dl.file_name_part, 'wb') as o_f:
                o_f.write(i_f.read(chunk[0]))
            remove(f'{dl.file_name_part}.temp')
            dl.progress = index
            dl.chunk_indexes = dl.chunk_indexes[index:]
            break           
        index += 1    

def check_for_existing_file(dl):
    if (path.exists(dl.file_name_part)):
        if (dl.file_size != path.getsize(dl.file_name_part)):
            set_download_progress(dl)
            print(f'[*] Partial File Found. Resuming Progress at chunk: {dl.progress} / {dl.num_of_chunks}')

    if (path.exists(dl.file_name)):
        if (dl.file_size == path.getsize(dl.file_name)):
            print('[+] File download is already complete')
            print_sha256(dl.file_name)
            exit()
        else:
            print('[-] Please manually delete file remnants and try again.')
            exit()
    
def write_file_to_disk(dl):
    with open(dl.file_name_part, 'ab') as file_on_disk:
        dl.session = requests.Session()
        start_time = time()
        dl.begin_download(file_on_disk)
        end_time = time()
    
    if (path.getsize(dl.file_name_part) == dl.file_size):
        rename(dl.file_name_part, dl.file_name)
        print(f'[+] Download completed in: {end_time - start_time} seconds')
        print_sha256(dl.file_name)

try:
    web_url = sys.argv[1]
    dl = Download(web_url)
    check_for_existing_file(dl)
    print(f'[+] Downloading file: {dl.file_name}')
    print(f'[+] File size: {dl.file_size_mb} MB')
    print(f'[+] Number of chunks set to: {dl.num_of_chunks}')
    write_file_to_disk(dl)
except IndexError:
    print('[-] Missing argument')
except KeyError:
    print('[-] Missing header: Content-Length')
except requests.exceptions.MissingSchema:
    print('[-] Argument is not a valid URL')
except requests.exceptions.ConnectionError:
    print('\n[-] Connection lost')
    print(f'[*] Chunks completed: {dl.progress} / {dl.num_of_chunks}')
except KeyboardInterrupt:
    print('\n[-] Script execution cancelled')
    print(f'[*] Chunks completed: {dl.progress} / {dl.num_of_chunks}')
except:
    print("[-] An unknown error has occured")