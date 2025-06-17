import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import re
import os
import zipfile
import shutil

# --- Configuration ---
BASE_DOMAIN = "https://www.masstamilan.dev"
SEARCH_URL_PATTERN = f"{BASE_DOMAIN}/search?keyword="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

# --- Helper Function ---
def get_page_soup(url, max_retries=3):
    """Fetches a page and returns a BeautifulSoup object with retries."""
    for attempt in range(max_retries):
        try:
            print(f"Fetching: {url}")
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}/{max_retries}: Error fetching {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return None

# --- Main Functions ---

def search_movie_and_get_page_url(movie_name):
    """
    Searches for a movie and returns a list of potential movie matches (title, url).
    Each item in the list is a dictionary: {'title': 'Movie Title', 'url': 'https://...'}
    """
    encoded_movie_name = urllib.parse.quote_plus(movie_name)
    search_url = f"{SEARCH_URL_PATTERN}{encoded_movie_name}"
    
    search_soup = get_page_soup(search_url)
    if not search_soup:
        print(f"Error: Could not fetch search results for '{movie_name}'.")
        return [] # Return empty list if fetch fails

    movie_links = search_soup.select('div.gw div.a-i a')
    
    potential_matches = []
    search_terms = re.split(r'\W+', movie_name.lower()) # Split by non-alphanumeric, lowercase

    for link in movie_links:
        href = link.get('href')
        link_identifier = (link.get('title') or link.get_text()).strip()

        if href:
            full_href = href if href.startswith('http') else BASE_DOMAIN + href
            path = urllib.parse.urlsplit(full_href).path

            # Only consider links that are movie/album pages from the base domain
            if full_href.startswith(BASE_DOMAIN) and '-songs' in path:
                current_score = 0
                for term in search_terms:
                    if term and term in link_identifier.lower():
                        current_score += 1
                
                # Consider a match if at least one search term is found
                # Or if the movie_name is directly in the identifier (for single-word names)
                if current_score > 0 or (len(search_terms) == 1 and search_terms[0] in link_identifier.lower()):
                    potential_matches.append({
                        'title': link_identifier,
                        'url': full_href,
                        'score': current_score # Keep score for potential sorting if needed
                    })
    
    # Sort matches by score in descending order to show best matches first
    potential_matches.sort(key=lambda x: x['score'], reverse=True)

    # Remove duplicates based on URL (some sites might list same movie multiple times)
    seen_urls = set()
    unique_matches = []
    for match in potential_matches:
        if match['url'] not in seen_urls:
            unique_matches.append(match)
            seen_urls.add(match['url'])

    return unique_matches


def get_download_link_by_quality(movie_page_url, desired_quality_string):
    """
    Navigates to a movie's page and extracts the download link and its text for the desired quality.
    Returns (download_link, link_text) or (None, None).
    """
    movie_soup = get_page_soup(movie_page_url)
    if not movie_soup:
        print(f"Error: Could not fetch movie page: {movie_page_url}")
        return None, None

    download_links = movie_soup.select('h2.za.normal a.dlink')

    target_download_link = None
    target_link_text = None 
    print(f"  Searching for '{desired_quality_string}' link on movie page...")

    for link in download_links:
        href = link.get('href')
        text = link.get_text().strip()

        if href:
            full_download_href = href if href.startswith('http') else BASE_DOMAIN + href

            if desired_quality_string.lower() in text.lower() and full_download_href.startswith(f"{BASE_DOMAIN}/downloader/"): 
                target_download_link = full_download_href
                target_link_text = text 
                print(f"  Found '{desired_quality_string}' link text: '{text}'")
                break
    
    if not target_download_link:
        print(f"Error: '{desired_quality_string}' download link not found on page: {movie_page_url}")
        return None, None
    
    return target_download_link, target_link_text 


# --- Main Execution ---
if __name__ == "__main__":
    movie_to_search = input("Enter the Tamil movie name to search for (e.g., Jailer): ")
    
    while True:
        quality_input = input("Enter desired quality (320 or 128): ").strip()
        if quality_input == '320':
            desired_quality_string = '320kbps'
            break
        elif quality_input == '128':
            desired_quality_string = '128kbps'
            break
        else:
            print("Invalid quality. Please enter '320' or '128'.")

    # Set base directory for downloads (no need to ask user for this part)
    custom_download_base_dir = os.path.expanduser("~/Music/Tamil")
    
    print(f"Searching for movie: '{movie_to_search}' with quality: '{desired_quality_string}'")

    # Get potential movie matches
    potential_movies = search_movie_and_get_page_url(movie_to_search)

    selected_movie_url = None
    selected_movie_title_for_folder = None # New variable for folder naming

    if not potential_movies:
        print("No movies found matching your search. Please try a different name.")
    elif len(potential_movies) == 1:
        print(f"Found one exact match: '{potential_movies[0]['title']}'. Proceeding with this.")
        selected_movie_url = potential_movies[0]['url']
        selected_movie_title_for_folder = potential_movies[0]['title'] # Use this for default folder name
    else:
        print("\nMultiple movies found. Please select the correct one:")
        for i, movie in enumerate(potential_movies):
            print(f"{i+1}. {movie['title']}")
        
        while True:
            try:
                choice = int(input(f"Enter the number of your choice (1-{len(potential_movies)}): "))
                if 1 <= choice <= len(potential_movies):
                    selected_movie_url = potential_movies[choice - 1]['url']
                    selected_movie_title_for_folder = potential_movies[choice - 1]['title'] # Use this for default folder name
                    print(f"You selected: '{selected_movie_title_for_folder}'")
                    break
                else:
                    print("Invalid number. Please enter a number within the range.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    if selected_movie_url:
        # Ask for the custom folder name for the extracted songs
        default_folder_name = re.sub(r'[^\w\s-]', '', selected_movie_title_for_folder or movie_to_search).strip().replace(' ', '_')
        
        # Ensure default_folder_name is not empty or just hyphens/underscores
        if not default_folder_name or re.fullmatch(r'[_ -]+', default_folder_name):
            default_folder_name = "Downloaded_Songs" # Fallback if clean title is empty
            
        custom_folder_name_input = input(
            f"Enter the name for the songs folder (default: '{default_folder_name}'): "
        ).strip()
        
        if custom_folder_name_input:
            # Clean the user-provided folder name as well
            clean_movie_name = re.sub(r'[^\w\s-]', '', custom_folder_name_input).strip().replace(' ', '_')
            if not clean_movie_name: # Fallback if user provides un-cleanable input
                clean_movie_name = default_folder_name
        else:
            clean_movie_name = default_folder_name

        print(f"Songs will be saved in: '{os.path.join(custom_download_base_dir, clean_movie_name)}'")


        print(f"Navigating to movie page: {selected_movie_url}")
        final_download_link, link_text_for_filename = get_download_link_by_quality(selected_movie_url, desired_quality_string)
        
        if final_download_link:
            print(f"\n✅ Found {desired_quality_string} download link: {final_download_link}")
            
            confirm_download = input("Do you want to download this file? (yes/no): ").lower()
            if confirm_download == 'yes':
                print(f"Attempting to download the file...")
                try:
                    # Create the full path for the movie's songs
                    movie_output_dir = os.path.join(custom_download_base_dir, clean_movie_name)
                    os.makedirs(movie_output_dir, exist_ok=True) # Ensure movie-specific directory exists

                    # Determine filename for the ZIP file
                    match = re.search(r'(\d+kbps)\s+ZIP', link_text_for_filename, re.IGNORECASE)
                    if match:
                        quality_part = match.group(1) 
                        zip_filename = f"{clean_movie_name}_{quality_part}.zip"
                    else:
                        zip_filename = f"{clean_movie_name}_{desired_quality_string}.zip"

                    zip_filepath = os.path.join(movie_output_dir, zip_filename)
                    
                    if os.path.exists(zip_filepath):
                        print(f"File '{zip_filename}' already exists. Skipping download.")
                    else:
                        print(f"Downloading ZIP to: {zip_filepath}")
                        with open(zip_filepath, "wb") as f_out:
                            file_content = requests.get(final_download_link, headers=HEADERS, stream=True)
                            file_content.raise_for_status() 
                            for chunk in file_content.iter_content(chunk_size=8192):
                                f_out.write(chunk)
                        print(f"Successfully downloaded {zip_filename}")
                        
                        # --- Extract and Delete ZIP ---
                        print(f"Extracting '{zip_filename}'...")
                        try:
                            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                                zip_ref.extractall(movie_output_dir) 
                            print(f"Successfully extracted contents to '{movie_output_dir}'")
                            
                            print(f"Deleting original ZIP file: '{zip_filename}'...")
                            os.remove(zip_filepath)
                            print(f"Successfully deleted '{zip_filename}'")
                        except zipfile.BadZipFile:
                            print(f"Warning: '{zip_filename}' is not a valid ZIP file. Cannot extract.")
                        except Exception as e:
                            print(f"Error during extraction or deletion: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to download {final_download_link}: {e}")
                except Exception as e:
                    print(f"An error occurred during download: {e}")
            else:
                print("Download skipped by user.")
        else:
            print("Could not find the specified quality download link for the movie.")
    else:
        print("Could not proceed without a selected movie page.")