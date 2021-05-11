import pafy, requests, os
from pathlib import Path
from tqdm import tqdm

print(os.curdir)

def download(link):
  video = pafy.new(link)
  streams = video.streams
  quality = None
  while True:
    for pos, stream in enumerate(streams):
      print(f'{pos}. ', stream.quality)
    print("Choose video quality (Enter 1, 2, ..etc): ")
    try:
      num = int(input()) - 1
      quality = streams[num]
    except Exception:
      print(f"Wrong input!.. please enter number from 1 to {pos+1}.")
    if quality != None:
      break
  print(quality)
  url = quality.url
  file = quality.generate_filename()
  initial_pos = 0
  try:
    file_size = Path(file).stat().st_size
    resume_headers ={'Range':f'bytes={file_size}-'}
    print('file_size = ', file_size)
    res = requests.get(url, stream=True, headers=resume_headers)
    total_size = int(res.headers.get('content-length'))
    print("Download resumed..!\n")
    with open(file,'ab') as f:
      with tqdm(total=total_size, unit='B',
        unit_scale=True,
        desc=file,initial=file_size,
        ascii=True) as pbar:
          for ch in res.iter_content(chunk_size=1024):
            if ch:
                f.write(ch) 
                pbar.update(len(ch))
  except FileNotFoundError:
    res = requests.get(url, stream=True)
    total_size = int(res.headers.get('content-length'))
    print("Download started..!\n")
    with open(file,'ab') as f:
      with tqdm(total=total_size, unit='B',
        unit_scale=True,
        desc=file,initial=initial_pos,
        ascii=True) as pbar:
          for ch in res.iter_content(chunk_size=1024):
            if ch:
                f.write(ch) 
                pbar.update(len(ch))

  print('Download finished.!')

if __name__ == '__main__':
  link = input("Enter Youtube video url: ")
  download(link)

