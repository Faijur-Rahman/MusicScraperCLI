from utils import get_page_soup
import re

def get_song_list(movie_page_url):
    soup = get_page_soup(movie_page_url)
    if not soup:
        return []
    songs = []
    for row in soup.find_all('tr', itemprop='itemListElement'):
        name_tag = row.find('span', itemprop='name')
        name = name_tag.a.get_text(strip=True) if name_tag and name_tag.a else 'Unknown'
        singer_tag = row.find('span', itemprop='byArtist')
        singers = singer_tag.get_text(strip=True) if singer_tag else 'Unknown'
        songs.append({'name': name, 'singers': singers})
    return songs

def get_download_link_by_quality(movie_page_url, quality_str):
    soup = get_page_soup(movie_page_url)
    if not soup:
        return None, None

    container = soup.select_one('h2.za.normal')
    if not container:
        return None, None

    links = container.find_all('a', class_='dlink')
    num = re.search(r'(\d+)', quality_str)
    if not num:
        return None, None

    identifiers = [f"zip{num.group(1)}", f"{num.group(1)}kbps", f"{num.group(1)}k"]
    for link in links:
        href, text = link.get('href'), link.get_text().strip()
        if href and any(x in href.lower() for x in identifiers):
            return href, text

    return None, None

def get_single_song_download_link(movie_page_url, song_title, quality_str):
    soup = get_page_soup(movie_page_url)
    if not soup:
        return None, None

    for row in soup.find_all('tr', itemprop='itemListElement'):
        tag = row.find('span', itemprop='name')
        if tag and tag.a and tag.a.get_text(strip=True).lower() == song_title.lower():
            links = row.find_all('a', class_='dlink')
            for link in links:
                href, text = link.get('href'), link.get_text().strip()
                if href and quality_str in text.lower():
                    return href, text
    return None, None
