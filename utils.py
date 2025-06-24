import yt_dlp
import os
import uuid

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_video(url):
    video_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")

    ydl_opts = {
        "format": "bv*+ba/best",
        "outtmpl": output_path,
        "merge_output_format": "mp4",
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "cookiefile": os.path.join(
            os.path.dirname(__file__), "cookies.txt"
        ),  # 👈 agregado
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return f"{video_id}.mp4"
