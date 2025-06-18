import os

def prompt_language_choice():
    while True:
        lang = input("Enter language (Tamil/Malayalam): ").strip().lower()
        if lang == 'tamil':
            return lang, "https://www.masstamilan.dev", os.path.expanduser("~/Music/Tamil")
        elif lang == 'malayalam':
            return lang, "https://mp3chetta.com", os.path.expanduser("~/Music/Malayalam")
        else:
            print("Invalid choice. Try again.")

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
