# 📂 Script Collection: File Management and YouTube Utilities

## 🌟 Overview

This repository contains four Python scripts designed to simplify file management and automate tasks related to YouTube playlists. From converting subtitles to downloading videos or audio, these scripts are efficient and easy to use.

---

## 🛠 Scripts

### 1. **Subtitle Converter (SRT to TXT)**

📄 This script converts `.srt` subtitle files into clean `.txt` files by removing:
- **Timestamps**
- **Line numbers**
- **Text in square brackets** (e.g., `[music]`).

**How to use**:
1. Place `.srt` files in the `subtitles/` folder.
2. Run the script to generate `.txt` files in `subtitles/TXT`.

---

### 2. **YouTube Subtitle Downloader**

🎥 Downloads and processes subtitles from YouTube playlists:
- Saves subtitles in `.vtt` format.
- Converts `.vtt` to `.srt`.
- Cleans `.srt` files by removing duplicates and unnecessary text.

**How to use**:
1. Enter the playlist URL.
2. Specify desired subtitle languages (e.g., `en`, `ru`).
3. Cleaned `.srt` files are saved in the `subtitles/` folder.

---

### 3. **YouTube Video and Audio Downloader**

⬇️ Downloads videos and audio tracks from YouTube playlists:
- **Videos**: Download in specific resolutions (e.g., `720p`, `1080p`).
- **Audio**: Extract high-quality audio tracks.
- Handles failed downloads and prevents overwriting existing files.

**How to use**:
1. Enter the playlist URL.
2. Choose to download videos or audio.
3. Files are saved in `Video/` or `Audio/` folders.

---

### 4. **Batch File Renamer**

✏️ Renames files in the same directory as the script by removing a specified number of characters from the beginning of each filename.

**How to use**:
1. Place the script in the target directory.
2. Enter the number of characters to remove.
3. Preview the changes and confirm before applying.

---

## ⚙️ Prerequisites

Ensure the following tools are installed on your system:

- **Python 3.6 or higher**
- **yt-dlp**: Install via pip:
  ```bash
  pip install yt-dlp
