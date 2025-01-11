Script Collection: File Management and YouTube Utilities
Overview
This repository contains four Python scripts designed for efficient file management and working with YouTube playlists. These scripts are user-friendly, handle edge cases, and automate common tasks like subtitle conversion, video/audio downloading, and batch file renaming.

Scripts
1. Subtitle Converter (SRT to TXT)
Converts .srt subtitle files to clean .txt files by removing:

Timestamps
Line numbers
Text in square brackets (e.g., [music]).
Usage:

Place .srt files in the subtitles folder.
Run the script to generate .txt files in subtitles/TXT.
2. YouTube Subtitle Downloader
Downloads subtitles from a YouTube playlist and performs the following:

Saves .vtt subtitles for selected languages.
Converts .vtt files to .srt.
Cleans .srt files by removing duplicates and unnecessary text.
Usage:

Enter the playlist URL and desired subtitle languages (e.g., en, ru).
Converted .srt files are saved in the subtitles folder.
3. YouTube Video and Audio Downloader
Downloads videos and audio tracks from a YouTube playlist:

Videos: Select desired resolution (e.g., 720p, 1080p).
Audio: Extract the best available quality.
Prevents overwriting and logs any failed downloads.
Usage:

Enter the playlist URL.
Choose to download videos or audio.
Files are saved in Video/ or Audio/ folders.
4. Batch File Renamer
Renames files in the script's directory by removing a specified number of characters from the beginning of each filename.

Usage:

Place the script in the target directory.
Enter the number of characters to remove.
Preview changes and confirm before applying.
Prerequisites
Python 3.6 or higher
yt-dlp: Install using pip install yt-dlp
ffmpeg: Download from ffmpeg.org and add to PATH (required for subtitle and video/audio processing).
How to Run
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/your-repo.git
cd your-repo
Run the desired script:

bash
Copy code
python script_name.py
Notes
All scripts include error handling to ensure stability.
Logs for failed downloads or skipped files are created automatically.
Ensure ffmpeg is installed and configured for video/audio processing.
