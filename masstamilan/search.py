import urllib.parse
import re
from utils import get_page_soup

def search_movie_and_get_page_url(movie_name, base_domain, search_url_pattern):
    encoded_movie_name = urllib.parse.quote_plus(movie_name)
    search_url = f"{search_url_pattern}{encoded_movie_name}"
    soup = get_page_soup(search_url)
    if not soup:
        return []

    movie_links = soup.select('div.gw div.a-i a')
    search_terms = re.split(r'\W+', movie_name.lower())
    potential_matches = []

    for link in movie_links:
        href = link.get('href')
        title = (link.get('title') or link.get_text()).strip()
        if href:
            full_href = href if href.startswith('http') else base_domain + href
            path = urllib.parse.urlsplit(full_href).path
            if full_href.startswith(base_domain) and '-songs' in path:
                score = sum(term in title.lower() for term in search_terms)
                if score:
                    potential_matches.append({'title': title, 'url': full_href, 'score': score})

    seen = set()
    results = []
    for match in sorted(potential_matches, key=lambda x: x['score'], reverse=True):
        if match['url'] not in seen:
            seen.add(match['url'])
            results.append(match)

    return results
