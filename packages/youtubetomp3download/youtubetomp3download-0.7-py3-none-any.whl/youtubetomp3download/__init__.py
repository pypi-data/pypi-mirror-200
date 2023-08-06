import os
from pytube import YouTube


def youtube_to_mp3(url: str):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    destination = '.'
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return yt.title, "has been successfully downloaded"