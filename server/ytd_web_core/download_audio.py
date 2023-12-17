from ytd_web_core.models import Downloadable
from pytube import YouTube as yt
from pytube import Stream
from ytd_web_core import cache_folder as global_cache_folder
from ytd_web_core.exceptions import AgeRestrictedVideoException, UnavailableVideoQualityException
from typing import Optional
from time import time
import os

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
