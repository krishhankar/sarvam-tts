import yt_dlp
from pathlib import Path

ENG_URL = "urls/eng_yt_urls.txt"
TAMIL_URL = "urls/tamil_yt_urls.txt"

def download_urls(url_file, audio_dir):
    Path(f"dataset/downloads/{audio_dir}").mkdir(parents=True, exist_ok=True)

    with open(url_file, "r") as f:
        urls = [line.strip() for line in f]
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"dataset/downloads/{audio_dir}/%(id)s.%(ext)s",
        "download_archive": f"dataset/{audio_dir}_downloaded.txt",
        "ignoreerrors": True,
        "continuedl": True,
        "retries": 5,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

    print(f"{audio_dir}: Finished downloading.")


download_urls(ENG_URL, "english")
download_urls(TAMIL_URL, "tamil")


