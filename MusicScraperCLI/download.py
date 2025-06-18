import os
import re
import requests
import zipfile
from urllib.parse import urljoin
from tqdm import tqdm
from config import HEADERS

def download_zip_album(url, quality_str, output_dir, movie_name):
    from extract import get_download_link_by_quality

    link, label = get_download_link_by_quality(url, quality_str)
    if not link:
        print("Album download link not found.")
        return

    if link.startswith("/"):
        link = urljoin(url, link)

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{movie_name}_{quality_str}.zip"
    filepath = os.path.join(output_dir, filename)

    print(f"Downloading album to {filepath}...")
    res = requests.get(link, headers=HEADERS, stream=True)
    total_size = int(res.headers.get('content-length', 0))
    with open(filepath, "wb") as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=filename, ascii=True) as bar:
        for chunk in res.iter_content(8192):
            f.write(chunk)
            bar.update(len(chunk))

    print("Extracting ZIP...")
    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        os.remove(filepath)
        print("Download and extraction complete.")
    except zipfile.BadZipFile:
        print("Invalid ZIP file.")

def download_single_song(url, title, quality_str, output_dir):
    from extract import get_single_song_download_link

    link, label = get_single_song_download_link(url, title, quality_str)
    if not link:
        print("Download link not found.")
        return

    if link.startswith("/"):
        link = urljoin(url, link)

    os.makedirs(output_dir, exist_ok=True)
    name = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')
    filename = f"{name}_{quality_str}.mp3"
    filepath = os.path.join(output_dir, filename)

    print(f"Downloading song to {filepath}...")
    res = requests.get(link, headers=HEADERS, stream=True)
    total_size = int(res.headers.get('content-length', 0))
    with open(filepath, "wb") as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=filename, ascii=True) as bar:
        for chunk in res.iter_content(8192):
            f.write(chunk)
            bar.update(len(chunk))
    print("Download complete.")
