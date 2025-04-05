
import subprocess


def download_video(url: str):
    cmd = [
        "yt-dlp",
        f"{url}"
    ]
    res = subprocess.run(cmd, capture_output=True)
    return res
