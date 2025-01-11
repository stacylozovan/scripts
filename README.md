📂 Script Collection: File Management and YouTube Utilities
🌟 Overview
This repository contains four Python scripts designed to simplify file management and automate tasks related to YouTube playlists. From converting subtitles to downloading videos or audio, these scripts are efficient and easy to use.

🛠 Scripts
1. Subtitle Converter (SRT to TXT)
📄 Converts .srt subtitle files into clean .txt files by removing:

Timestamps
Line numbers
Text in square brackets (e.g., [music]).
📌 Usage:

Place .srt files in the subtitles/ folder.
Run the script to generate .txt files in subtitles/TXT.
2. YouTube Subtitle Downloader
🎥 Downloads and processes subtitles from YouTube playlists:

Saves .vtt subtitles in selected languages.
Converts .vtt to .srt.
Cleans .srt files by removing duplicates and unnecessary text.
📌 Usage:

Enter the playlist URL.
Specify desired subtitle languages (e.g., en, ru).
Cleaned .srt files are saved in the subtitles/ folder.
3. YouTube Video and Audio Downloader
⬇️ Downloads videos and audio tracks from YouTube playlists:

Videos: Download in a specific resolution (e.g., 720p, 1080p).
Audio: Extract high-quality audio tracks.
Handles failed downloads and prevents overwriting existing files.
📌 Usage:

Enter the playlist URL.
Choose to download videos or audio.
Files are saved in Video/ or Audio/ folders.
4. Batch File Renamer
✏️ Renames files in the same directory as the script by removing a specified number of characters from the beginning of each filename.

📌 Usage:

Place the script in the target directory.
Enter the number of characters to remove.
Preview the changes and confirm before applying.
⚙️ Prerequisites
Ensure the following tools are installed on your system:

Python 3.6 or higher
yt-dlp: Install via pip:
bash
Copy code
pip install yt-dlp
ffmpeg: Download and add to PATH from ffmpeg.org.
🚀 How to Run
Clone this repository:

bash
Copy code
git clone https://github.com/yourusername/your-repo.git
cd your-repo
Run the desired script:

bash
Copy code
python script_name.py
📝 Notes
All scripts include error handling for stability.
Failed downloads and skipped files are logged automatically.
Ensure ffmpeg is correctly installed for video/audio processing.
📁 Directory Structure
plaintext
Copy code
├── scripts/
│   ├── subtitles/
│   │   ├── TXT/           # Cleaned .txt subtitle files
│   │   └── .srt files     # Original subtitle files
│   ├── Video/             # Downloaded videos
│   ├── Audio/             # Downloaded audio tracks
│   └── errors.txt         # Log file for failed downloads
💡 Tip: Combine these scripts to handle subtitle processing, video/audio downloads, and file management seamlessly.

🎉 Happy automating! 😊
