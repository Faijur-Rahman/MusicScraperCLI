import os

def prompt_language_choice():
    # 1. Select Language
    while True:
        lang = input("Enter language (Tamil/Malayalam/Hindi/Telugu): ").strip().lower()
        
        # Define defaults based on OS and Language
        home_dir = os.path.expanduser("~")
        
        if lang == 'tamil':
            base_url = "https://www.masstamilan.dev"
            default_path = os.path.join(home_dir, "Music", "Tamil")
            break
        elif lang == 'malayalam':
            base_url = "https://mp3chetta.com"
            default_path = os.path.join(home_dir, "Music", "Malayalam")
            break
        elif lang == 'hindi':
            base_url = "https://mp3bhai.com"
            default_path = os.path.join(home_dir, "Music", "Hindi")
            break
        elif lang == 'telugu':
            base_url = "https://masstelugu.com"
            default_path = os.path.join(home_dir, "Music", "Telugu")
            break
        else:
            print("Invalid choice. Try again.")

    # 2. Option to Change Output Folder
    print(f"\nDefault output folder: {default_path}")
    change_folder = input("Do you want to change this folder? (y/N): ").strip().lower()

    if change_folder == 'y':
        while True:
            new_path = input("Enter full path for downloads: ").strip()
            # Remove surrounding quotes if user pasted path like "C:\Users\Name"
            new_path = new_path.replace('"', '').replace("'", "")
            
            if new_path:
                # Normalize path separators for Windows/Linux
                final_path = os.path.normpath(new_path)
                print(f"Output folder set to: {final_path}\n")
                return lang, base_url, final_path
            else:
                print("Path cannot be empty.")
    else:
        print(f"Using default folder.\n")
        return lang, base_url, default_path

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
