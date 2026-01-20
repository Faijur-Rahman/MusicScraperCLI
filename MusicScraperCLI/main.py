# main.py
from prompts import prompt_language_choice, prompt_quality_choice, prompt_movie_selection, prompt_album_or_single_choice
from search import search_movie_and_get_page_url
from extract import get_song_list
from download import download_zip_album, download_single_song
import os
import re
import sys

def main():
    # Force UTF-8 encoding for Windows terminals to handle symbols like '▶'
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    language_choice, BASE_DOMAIN, download_base_dir = prompt_language_choice()
    SEARCH_URL_PATTERN = f"{BASE_DOMAIN}/search?keyword="

    movie_to_search = input("Enter the movie name to search for: ")
    desired_quality_string = prompt_quality_choice()

    potential_movies = search_movie_and_get_page_url(movie_to_search, BASE_DOMAIN, SEARCH_URL_PATTERN)
    selected_movie_url, selected_movie_title = prompt_movie_selection(potential_movies, movie_to_search)

    if not selected_movie_url:
        print("Could not proceed without a selected movie page.")
        return

    # Sanitize inputs to ensure valid Windows folder names
    default_folder_name = re.sub(r'[^\w\s-]', '', selected_movie_title or movie_to_search).strip().replace(' ', '_') or "Downloaded_Songs"
    folder_name = input(f"Enter folder name for saving songs (default: {default_folder_name}): ").strip() or default_folder_name
    
    # Extra sanitization for the final folder path
    clean_folder_name = re.sub(r'[^\w\s-]', '', folder_name).strip().replace(' ', '_')
    output_dir = os.path.join(download_base_dir, clean_folder_name)

    download_type = prompt_album_or_single_choice()

    if download_type == 'a':
        download_zip_album(selected_movie_url, desired_quality_string, output_dir, clean_folder_name)
    else:
        songs = get_song_list(selected_movie_url)
        if not songs:
            print("No songs found.")
            return

        print("\nAvailable songs on this album:")
        for i, song in enumerate(songs):
            print(f"{i+1}. {song['name']} (Singers: {song['singers']})")

        while True:
            selection_input = input(f"Enter song numbers to download (e.g. 1,3,5): ").strip()
            try:
                indices = [int(x.strip()) - 1 for x in selection_input.split(',') if x.strip()]
                if all(0 <= idx < len(songs) for idx in indices):
                    break
                else:
                    print("One or more numbers out of range.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")

        for idx in indices:
            song_name = songs[idx]['name']
            print(f"\n▶ Downloading: {song_name}")
            download_single_song(selected_movie_url, song_name, desired_quality_string, output_dir)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # This block catches Ctrl+C
        print("\n\nBye!!!")
        sys.exit(0)
