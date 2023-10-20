import os
from pytube import YouTube as yt
from pytube import Stream
from os import mkdir
import subprocess
from subprocess import run as cmd
from ytd_web_core.exceptions import VideoProcessingFailureException, AgeRestrictedVideoException
from ytd_web_core.util import get_name
from ytd_web_core import cache_folder as global_cache_folder
from typing import Optional
from ytd_web_core.models import Downloadable
from time import time

def has_audio(filename):
    result = subprocess.run(
        [
            "ffprobe", 
            "-v", "error", 
            "-show_entries",
            "format=nb_streams", "-of",
            "default=noprint_wrappers=1:nokey=1", 
            filename
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    return (int(result.stdout) -1)

def download_video(video_link: str, reso: str) -> Downloadable:
    is_needed_to_be_encoded = False
    try:
        is_needed_to_be_encoded = int(reso.split("p")[0]) > 720
    except Exception:
        is_needed_to_be_encoded = True

    yt_vid = yt(video_link)
    if (yt_vid.age_restricted):
        raise AgeRestrictedVideoException
    vid_file: Optional[Stream] = yt_vid.streams.filter(res=str(reso)).first()
    aud_file: Optional[Stream]
    
    cache_folder = global_cache_folder + "/" + str(time())
    in_vid: str = f"{cache_folder}/yt_temp/vid"
    in_aud: str = f"{cache_folder}/yt_temp/aud"
    out: str = f"{cache_folder}/yt_temp/final"
    out_file: str = vid_file.download(in_vid)

    is_needed_to_be_encoded = not has_audio(out_file)

    if is_needed_to_be_encoded:
        aud_file = yt_vid.streams.filter(only_audio=True).first()
        name: str = get_name()

        try:
            os.rename(out_file, in_vid + "/" + name)
        except FileExistsError:
            os.remove(in_vid + name)
            os.rename(out_file, in_vid + "/" + name)
        aud_file.download(in_aud, name)

        try:
            mkdir(out)
        except FileExistsError:
            pass

        try:               
            stream: str = name
            ffmpeg_command = 'ffmpeg -i "'+str(in_vid)+'/'+str(stream)+'" -i "'+str(in_aud)+'/'+str(stream)+'" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -y "'+str(out)+'/'+str(stream)+'"'
            cmd(str(ffmpeg_command) ,shell=True)
            try:
                os.rename(out + '/' + name, out_file)
            except FileExistsError:
                os.remove(out_file)
                os.rename(out + '/' + name, out_file)
        except FileNotFoundError:
            raise VideoProcessingFailureException()
        except Exception as e:
            raise VideoProcessingFailureException(str(e))
        
    downloadable = Downloadable(
        path=out_file, 
        name=out_file.split("/")[-1],
        folder=cache_folder
    )
    downloadable.save()
    downloadable.initInvalidation()

    return downloadable
