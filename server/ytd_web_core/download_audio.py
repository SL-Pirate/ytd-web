from ytd_web_core.models import Downloadable
from pytube import YouTube as yt
from yt_dlp import YoutubeDL
from pytube import Stream
from ytd_web_core import cache_folder as global_cache_folder
from ytd_web_core.util import depricated
from ytd_web_core.exceptions import AgeRestrictedVideoException, UnavailableVideoQualityException
from typing import Optional
from time import time
import os

@depricated()
def download_audio(
        video_link: str, 
        reso: str,
    ) -> Downloadable:
    yt_vid = yt(video_link)
    if (yt_vid.age_restricted):
        raise AgeRestrictedVideoException
    aud_file: Optional[Stream] = yt_vid.streams.filter(only_audio=True, abr=str(reso)).first()

    if aud_file is None:
        raise UnavailableVideoQualityException
    
    cache_folder = global_cache_folder + "/" + str(time())
    tmp_out_file: str = aud_file.download(f"{cache_folder}/yt_temp/final")
    pre, ext = os.path.splitext(tmp_out_file)
    out_file = tmp_out_file.replace(ext, ".mp3")
    try:
        os.rename(tmp_out_file, pre + ".mp3")
    except FileExistsError:
        os.remove(out_file)
        os.rename(tmp_out_file, pre + ".mp3")
        
    downloadable = Downloadable(
        path=out_file, 
        name=out_file.split("/")[-1],
        folder=cache_folder
    )
    downloadable.save()
    downloadable.initInvalidation()

    return downloadable

def download_audio_dl(
        video_link: str, 
        reso: str,
    ) -> Downloadable:
    cache_folder = global_cache_folder + "/" + str(time())

    format = "bestaudio/best"
    if reso is not None:
        format += f"[abr={reso.replace('kbps', '')}]"

    ydl_opts = {
        "format": format,
        "outtmpl": f"{cache_folder}/%(title)s",
        'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        },
        {
            'key': 'FFmpegMetadata'
        }, {
            'key': 'EmbedThumbnail'
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
            file_name = ydl.prepare_filename(ydl.extract_info(video_link, download=False))
    except OSError:
        # Handeling filename too long error
        ydl_opts['outtmpl'] = f'{cache_folder}/{str(time())}.%(ext)s'
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
            file_name = ydl.prepare_filename(ydl.extract_info(video_link, download=False))
        
    file_name += ".mp3"
    downloadable = Downloadable(
        path=file_name, 
        name=file_name.split("/")[-1],
        folder=cache_folder
    )
    downloadable.save()
    downloadable.initInvalidation()

    return downloadable
