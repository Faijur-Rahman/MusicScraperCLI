
# 🎵 Multi-Language Song Downloader

Download and Manage Songs Effortlessly 🎶

This Python script allows you to search for movie songs, select your desired audio quality (320kbps or 128kbps), download them, and automatically extract the songs into neatly organized folders. The original ZIP files are then cleaned up to keep your music library tidy.

---
[MusicScraperCLI-demo.webm](https://github.com/user-attachments/assets/7e66d333-da7a-4470-8272-8bb82b7d2ae0)


## ✨ Features

- **Search by Movie Name:** Easily find songs for your favorite movies.
- **Quality Selection:** Choose between **320kbps** and **128kbps** audio quality by simply entering `320` or `128`.
- **Smart Search Matching:** If multiple matches are found, the script presents a list of options, letting you pick the correct movie.
- **Automated Download Location:** All your downloaded and extracted music is saved to `~/Music/Language/` .
- **Organized Downloads:** Each movie's songs are extracted into a dedicated subfolder (e.g., `~/Music/Tamil/Jailer/`).
- **Automatic Extraction & Cleanup:** Downloads ZIP files, extracts the audio contents, and then deletes the original ZIP to save space.

---

## 🚀 Getting Started

Follow these simple steps to get the script up and running on your Linux system.

### 🧰 Prerequisites

You'll need **Python 3** installed. Check your version with:

```bash
python3 --version
```

Install the virtual environment module if not already installed:

For **Debian/Ubuntu**:
```bash
sudo apt update
sudo apt install python3-venv
```

For **Fedora/RHEL/CentOS**:
```bash
sudo dnf install python3-virtualenv
```

---

### 📥 Installation

#### 1. Clone the Repository (Recommended)

```bash
git clone https://github.com/Faijur-Rahman/MusicScraperCLI.git
cd MusicScraperCLI
```

#### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

#### 3. Activate the Virtual Environment

```bash
source venv/bin/activate
```

(You should see `(venv)` in your terminal prompt.)

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 How to Use

Once everything is set up:

1. Ensure your virtual environment is active:
   ```bash
   source venv/bin/activate
   ```

2. Run the script:
   ```bash
   python main.py
   ```

3. Follow the prompts:
   - Enter language (Tamil/Malayalam): (e.g., `Tamil`)
   - Enter the movie name to search for: (e.g., `Raja Rani`)
   - Enter the desired quality (`320` or `128`) (e.g., `320`)
   - If multiple matches are shown, 
   - Choose movie number: (select the correct one)
   - Enter folder name for saving songs (default: Jailer_tamil_songs_download): (e.g., `RajaRani_Songs`)
   - Download [A]lbum or [S]ingle song? (e.g., `A or S`)
   - If single song chosen and multiple matches are shown
   - Enter song numbers to download (e.g. `1,3,5`): 

Your songs will be saved under:

```
~/Music/Language/Your_Movie_Name/
```

---

### 📴 Deactivate the Environment

When you're done:

```bash
deactivate
```

---

## 🛠️ TODO

Here are some planned features and enhancements for future versions:

- [x] **Specific Song Download:** Ability to choose and download individual songs instead of full albums.
- [x] **Progress Bar:** Show download progress using a terminal progress bar (e.g., `tqdm`).
- [x] **Support for Other Languages:** Extend functionality to download Telugu, Hindi, or Malayalam songs from similar sources (Updated: Malayalam).
- [ ] **GUI Support:** Add a graphical user interface using Tkinter or PyQt for ease of use.
- [ ] **Error Logging:** Log failed downloads or extraction issues to a file for debugging.
- [ ] **Cross-Platform Improvements:** Enhance compatibility and download path handling for both Windows and Linux.

---

## ⚠️ Disclaimer & Ethical Use

This script is intended for **personal use** to automate access to publicly available content from **Masstamilan.dev**.

> Please respect the website's Terms of Service and copyright policies.
>
> Use this tool responsibly. The developer is not responsible for any misuse.

---
