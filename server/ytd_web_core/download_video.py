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
from enum import Enum

class VideoFormat(Enum):
    DEFAULT = ''
    MP4 = "mp4"
    WEBM = "webm"
    MKV = "mkv"

def _is_needed_to_be_encoded(
        filename: str, 
        required_format: VideoFormat,
        current_format: str
    ) -> bool:
    if (
        required_format != VideoFormat.DEFAULT 
        and str.lower(current_format) != str.lower(required_format.value)
    ):
        return True
    
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
    
    if (not (int(result.stdout) -1)):
        return True
    
    return False

def _process(
        name: str, 
        out: str, 
        out_file: str, 
        in_aud: str, 
        in_vid: str,
        video_codec: str = "copy",
    ):
    try:
        stream: str = name
        ffmpeg_command = 'ffmpeg -i "'+str(in_vid)+'/'+str(stream)+'" -i "'+str(in_aud)+'/'+str(stream)+'" -c:v ' + str(video_codec) + ' -c:a aac -map 0:v:0 -map 1:a:0 -y "'+str(out)+'/'+str(stream)+'"'
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

def download_video(
        video_link: str, 
        reso: str, 
        format: str = VideoFormat.DEFAULT.value
    ) -> Downloadable:
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

    # checking if the format is an available format
    for (key, value) in VideoFormat.__members__.items():
        if (format == value.value):
            format = value
            break

    # if (format is str):
    #     format = VideoFormat.DEFAULT

    # checking if needed to be processed
    current_format = out_file.split(".")[-1]
    if _is_needed_to_be_encoded(
        out_file, 
        format,
        current_format
    ):
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
        
        if format != VideoFormat.DEFAULT:
            out_file = out_file.replace(current_format, format.value)

        codec: str = "copy"
        if (reso == '144p'):
            codec = 'h264'

        _process(name, out, out_file, in_aud, in_vid, codec)

        
    downloadable = Downloadable(
        path=out_file, 
        name=out_file.split("/")[-1],
        folder=cache_folder
    )
    downloadable.save()
    downloadable.initInvalidation()

    return downloadable
