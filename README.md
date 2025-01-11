📂 Script Collection: File Management and YouTube Utilities
This repository contains four Python scripts designed to simplify file management and automate tasks related to YouTube playlists. From converting subtitles to downloading videos or audio, these scripts are efficient and easy to use.

🌟 Overview of Scripts
Subtitle Converter (SRT to TXT): This script converts .srt subtitle files into clean .txt files by removing timestamps, line numbers, and text in square brackets (e.g., [music]). Place .srt files in the subtitles/ folder, and the script will generate .txt files in subtitles/TXT.

YouTube Subtitle Downloader: This script downloads subtitles from YouTube playlists, saves them in .vtt format, converts them to .srt, and cleans the .srt files by removing duplicates and unnecessary text. To use, enter the playlist URL, specify the subtitle languages (e.g., en, ru), and the cleaned .srt files will be saved in the subtitles/ folder.

YouTube Video and Audio Downloader: This script downloads videos and audio tracks from YouTube playlists. It allows users to download videos in specific resolutions (e.g., 720p, 1080p) or extract high-quality audio tracks. The downloaded files are saved in Video/ or Audio/ folders. It handles failed downloads and prevents overwriting existing files.

Batch File Renamer: This script renames files in the same directory by removing a specified number of characters from the beginning of each filename. Place the script in the target directory, input the number of characters to remove, preview the changes, and confirm the renaming process.

⚙️ Prerequisites
Ensure the following tools are installed on your system: Python 3.6 or higher, yt-dlp (install via pip install yt-dlp), and ffmpeg (download and add to PATH from ffmpeg.org).

🚀 How to Use
Clone this repository using git clone https://github.com/yourusername/your-repo.git and navigate to the directory with cd your-repo. Run the desired script using python script_name.py. Follow the prompts provided by each script to input required information such as playlist URLs or file renaming parameters.

📝 Notes
These scripts include error handling to ensure stability. Failed downloads and skipped files are logged automatically in errors.txt. Ensure ffmpeg is installed for video and audio processing. The scripts also prevent overwriting files by checking for conflicts during the renaming or downloading process.
