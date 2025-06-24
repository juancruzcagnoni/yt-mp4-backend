import yt_dlp
import os
import uuid

# Detectar si estamos en Render (deployment)
IS_RENDER = os.environ.get("RENDER") is not None

# Usar '/tmp/downloads' en Render, 'downloads' localmente
BASE_DIR = "/tmp/downloads" if IS_RENDER else os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(BASE_DIR, exist_ok=True)

def download_youtube_video(url):
    video_id = str(uuid.uuid4())
    output_path = os.path.join(BASE_DIR, f"{video_id}.%(ext)s")

    ydl_opts = {
        "format": "bv*+ba/best",
        "outtmpl": output_path,
        "merge_output_format": "mp4",
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "cookiefile": os.path.join(os.path.dirname(__file__), "cookies.txt"),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return f"{video_id}.mp4"
