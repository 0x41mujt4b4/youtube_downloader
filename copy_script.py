import os, time, concurrent.futures, multiprocessing
from pathlib import Path
from itertools import accumulate
import shutil

os.chdir('/home/almujtaba/Desktop')
file = open('Tom.and.Jerry.2021.720p.Bluray.akwam.io.mp4', 'r')
file_size = Path('file.txt').stat().st_size
part1 = file_size//2
part2 = (file_size//2)+(file_size%2)


# first_text = ' '.join([str(i) for i in range(1, 10000000)])
# second_text = ' '.join([str(i) for i in range(10000001, 20000000)])
# third = first_text + second_text


# size = len(first_text + second_text)
# chunk = len(first_text)
# text = (first_text, second_text)

def write(start_point, bytes):
    with open('file_copy.txt', 'r+') as file:
        print(file.seek(start_point))
        print(f'i will write from {start_point} to {start_point+len(bytes)}.')
        file.writelines(bytes)
    print('Done writing.')

def Lambda(args):
    return write(*args)

def read(start_point, part_size):
    parts = []
    file.seek(start_point)
    part = file.read(part_size)
    return part

def parts(num_of_parts):
    size_of_parts = [file_size//num_of_parts for _ in range(num_of_parts-1)]
    size_of_parts.append((file_size//num_of_parts)+(file_size%num_of_parts))
    return size_of_parts

t1 = time.perf_counter()

parts_sizes = parts(2)

sizes = list(accumulate(parts_sizes))
sizes.insert(0, 0)
readable_sizes = list(zip(sizes, parts_sizes))
print(sizes)

parts = [read(*part) for part in readable_sizes]

files = list(zip(sizes, parts))
# for f in files:
#     print(f[0], len(f[1]))

with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
    results = executor.map(Lambda, files)


# write(0, third)

# task1 = multiprocessing.Process(target=write, args=[0, file1])
# task2 = multiprocessing.Process(target=write, args=[part1, file2])

# print(type(read(*parts[0])[0]))

# task1.start()
# task2.start()

# task1.join()
# task2.join()
t2 = time.perf_counter()
file.close()
print(f'finished in {t2-t1} seconds.')
