# from django.test import TestCase

# # Create your tests here.

# This is just a temporary file for testing purposes
# Not a unit test
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

def download_video_dl(
        video_link: str,
        reso: str=None
    ): # -> Downloadable:
    # cache_folder = global_cache_folder + "/" + str(time())
    cache_folder = "/home/slpirate/Downloads"

    if reso is not None:
        height = reso.split("p")[0]
    
    ydl_opts = {
        'format': f'bestvideo[height<={height}]+bestaudio/best[height<={height}]' 
            if reso is not None 
            else 'bestvideo+bestaudio/best',
        'outtmpl': f'{cache_folder}/%(title)s.%(ext)s',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

    # downloadable = Downloadable(
    #     path=f'', 
    #     name=out_file.split("/")[-1],
    #     folder=cache_folder
    # )

if __name__ == "__main__":
    # link = "https://fb.watch/p6pM2_16gm/?mibextid=6aamW6"
    link = "https://www.reddit.com/r/TKASYLUM/comments/18uwl2s/%E0%B7%84%E0%B6%BB%E0%B6%B1_%E0%B6%B4%E0%B6%9A_%E0%B6%85%E0%B6%B8%E0%B6%BB%E0%B7%80/"

    with YoutubeDL() as ydl:
        try:
            print(ydl.extract_info("invalid link", download=False))
        except DownloadError as e:
            print(str(e))

    download_video_dl(link)

