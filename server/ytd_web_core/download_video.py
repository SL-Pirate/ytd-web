import os
from pytube import YouTube as yt
from pytube import Stream
from os import mkdir
import subprocess
from subprocess import run as cmd
from ytd_web_core.exceptions import VideoProcessingFailureException, AgeRestrictedVideoException, UnavailableVideoQualityException
from ytd_web_core.util import get_name
from ytd_web_core import cache_folder as global_cache_folder
from typing import Optional
from ytd_web_core.models import Downloadable
from time import time
from enum import Enum
from yt_dlp import YoutubeDL
from ytd_web_core.util import depricated

class VideoFormat(Enum):
    DEFAULT = ''
    MP4 = "mp4"
    WEBM = "webm"
    MKV = "mkv"

def _is_needed_to_be_encoded(
        filename: str, 
        required_format: VideoFormat,
        current_format: str,
        reso: str = None
    ) -> bool:
    if (
        required_format != VideoFormat.DEFAULT 
        and str.lower(current_format) != str.lower(required_format.value)
    ):
        return True
    
    if (reso == '144p' or reso == '240p'):
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

@depricated()
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

    if vid_file is None:
        raise UnavailableVideoQualityException
    
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
        if (reso == '144p' or reso == '240p'):
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

def _extract_height(reso: str) -> int | None:
    value = None
    if 'p' in reso:
        value = reso.split('p')[0]
    elif 'x' in reso:
        value = reso.split('x')[1]
        
    if value is not None:
        try:
            return int(value)
        except ValueError:
            return None

def _get_format(reso: str | None) -> str:
    if reso is None:
        return 'bestvideo+bestaudio/best'
    height: str | None = str(_extract_height(reso))
    if height is None:
        return 'bestvideo+bestaudio/best'
    else:
        return f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'

def download_video_dl(
        video_link: str,
        reso: str,
        format: str = None
    ) -> Downloadable:
    cache_folder = global_cache_folder + "/" + str(time())
    file_name = str(time())

    ydl_opts = {
        'format': _get_format(reso),
        'outtmpl': f'{cache_folder}/%(title)s.%(ext)s',
        'quiet': True
    }

    if format is not None:
        ydl_opts["postprocessors"] = [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': format
            }
        ]

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

    if format is not None:
        current_format = file_name.split(".")[-1]
        file_name = file_name.replace(current_format, format)

    downloadable = Downloadable(
        path=file_name, 
        name=file_name.split("/")[-1],
        folder=cache_folder
    )
    downloadable.save()
    downloadable.initInvalidation()

    return downloadable
