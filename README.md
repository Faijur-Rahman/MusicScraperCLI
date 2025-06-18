# 🎵 Tamil Song Downloader

Download and Manage Tamil Songs Effortlessly 🎶

This Python script allows you to search for Tamil movie songs on [Masstamilan.dev](https://www.masstamilan.dev/), select your desired audio quality (320kbps or 128kbps), download them, and automatically extract the songs into neatly organized folders. The original ZIP files are then cleaned up to keep your music library tidy.

---

## ✨ Features

- **Search by Movie Name:** Easily find songs for your favorite Tamil movies.
- **Quality Selection:** Choose between **320kbps** and **128kbps** audio quality by simply entering `320` or `128`.
- **Smart Search Matching:** If multiple matches are found, the script presents a list of options, letting you pick the correct movie.
- **Automated Download Location:** All your downloaded and extracted music is saved to `~/Music/Tamil/` by default.
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
git clone https://github.com/Faijur-Rahman/masstamilan_scraper.git
cd masstamilan_scraper
```

Or download `masstamilan_scraper.py` directly and place it in your project folder.

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
pip install requests beautifulsoup4
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
   python masstamilan_scraper.py
   ```

3. Follow the prompts:
   - Enter the movie name (e.g., `Jailer`)
   - Enter the desired quality (`320` or `128`)
   - If multiple matches are shown, select the correct one
   - Confirm the download by typing `yes` or `no`

Your songs will be saved under:

```
~/Music/Tamil/Your_Movie_Name/
```

---

### 📴 Deactivate the Environment

When you're done:

```bash
deactivate
```

---

## 🪟 Running on Windows

Follow these steps if you're using **Windows**:

### 1. Install Python

- Download the latest version of Python 3 from the official site: https://www.python.org/downloads/windows/
- During installation, **make sure to check the box that says "Add Python to PATH"**

Verify installation:

```cmd
python --version
```

### 2. Install Virtual Environment (Optional but Recommended)

You can use Python’s built-in venv:

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

### 3. Install Dependencies

Make sure you're in the activated environment:

```cmd
pip install requests beautifulsoup4
```

### 4. Run the Script

In Command Prompt (or PowerShell):

```cmd
python masstamilan_scraper.py
```

Follow the on-screen prompts just like in Linux:
- Enter the movie name (e.g., `Jailer`)
- Enter `320` or `128` for the desired audio quality
- Confirm the movie selection
- Confirm download

Songs will be saved to:

```
C:\Users\YourUsername\Music\Tamil\Movie_Name\
```

Change the `custom_download_base_dir` in the script if you want to use a different folder.

---

## 📌 Notes for Windows Users

- If your download location (`~/Music/Tamil/`) causes issues, update the script with an absolute Windows path (e.g., `C:\TamilMusic\`).
- If `requests` or `beautifulsoup4` fail to install, try upgrading `pip` first:
  ```cmd
  python -m pip install --upgrade pip
  ```
---

## 🛠️ TODO

Here are some planned features and enhancements for future versions:

- [ ] **Specific Song Download:** Ability to choose and download individual songs instead of full albums.
- [ ] **Support for Other Languages:** Extend functionality to download Telugu, Hindi, or Malayalam songs from similar sources.
- [ ] **Multiple Sources Support:** Allow user to choose from different sites (e.g., Masstamilan.dev, Isaimini, TamilPaadal) if available.
- [ ] **GUI Support:** Add a graphical user interface using Tkinter or PyQt for ease of use.
- [ ] **Progress Bar:** Show download progress using a terminal progress bar (e.g., `tqdm`).
- [ ] **Error Logging:** Log failed downloads or extraction issues to a file for debugging.
- [ ] **Cross-Platform Improvements:** Enhance compatibility and download path handling for both Windows and Linux.
"""

---

## ⚠️ Disclaimer & Ethical Use

This script is intended for **personal use** to automate access to publicly available content from **Masstamilan.dev**.

> Please respect the website's Terms of Service and copyright policies.
>
> Use this tool responsibly. The developer is not responsible for any misuse.

---
