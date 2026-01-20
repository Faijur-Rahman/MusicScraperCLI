import os
import json

SETTINGS_FILE = "settings.json"

def load_settings():
    """Load settings from the JSON file if it exists."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_settings(settings):
    """Save the settings dictionary to the JSON file."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except IOError:
        print("Warning: Could not save settings file.")

def prompt_language_choice():
    # Load saved settings (or empty dict if none exist)
    settings = load_settings()
    
    # 1. Select Language
    while True:
        lang = input("Enter language (Tamil/Malayalam): ").strip().lower()
        
        if lang == 'tamil':
            base_url = "https://www.masstamilan.dev"
            # Separate keys so Tamil and Malayalam can have different saved folders
            settings_key = "tamil_path" 
            fallback_path = os.path.join(os.path.expanduser("~"), "Music", "Tamil")
            break
        elif lang == 'malayalam':
            base_url = "https://mp3chetta.com"
            settings_key = "malayalam_path"
            fallback_path = os.path.join(os.path.expanduser("~"), "Music", "Malayalam")
            break
        else:
            print("Invalid choice. Try again.")

    # 2. Determine the Current Path (Saved > Fallback)
    current_path = settings.get(settings_key, fallback_path)

    print(f"\nOutput folder: {current_path}")
    change_folder = input("Do you want to change this folder? (y/N): ").strip().lower()

    if change_folder == 'y':
        while True:
            new_path = input("Enter new full path: ").strip()
            # Remove quotes if user pasted a path from Windows "Copy as path"
            new_path = new_path.replace('"', '').replace("'", "")
            
            if new_path:
                final_path = os.path.normpath(new_path)
                
                # SAVE THE NEW PATH PERMANENTLY
                settings[settings_key] = final_path
                save_settings(settings)
                
                print(f"Folder updated and saved!\n")
                return lang, base_url, final_path
            else:
                print("Path cannot be empty.")
    else:
        # If user just hits Enter (N), use the persistent/current path
        print(f"Using current folder.\n")
        return lang, base_url, current_path

def prompt_quality_choice():
    while True:
        q = input("Enter desired quality (128 or 320): ").strip()
        if q in ('128', '320'):
            return f"{q}kbps"
        print("Invalid input.")

def prompt_movie_selection(matches, movie_name):
    if not matches:
        print(f"No results found for {movie_name}.")
        return None, None
    elif len(matches) == 1:
        print(f"Found: {matches[0]['title']}")
        return matches[0]['url'], matches[0]['title']
    else:
        for i, m in enumerate(matches):
            print(f"{i+1}. {m['title']}")
        while True:
            try:
                choice = int(input("Choose movie number: "))
                if 1 <= choice <= len(matches):
                    return matches[choice-1]['url'], matches[choice-1]['title']
            except ValueError:
                pass
            print("Invalid input.")

def prompt_album_or_single_choice():
    while True:
        c = input("Download [A]lbum or [S]ingle song? ").strip().lower()
        if c in ('a', 's'):
            return c
        print("Invalid input.")
