from pytube import YouTube as yt
from pytube.exceptions import AgeRestrictedError, RegexMatchError as InvalidYoutubeLinkError
from ytd_web_core.exceptions import AgeRestrictedVideoException
from yt_dlp import YoutubeDL
from ytd_web_core import YOUTUBE_DL_OPTIONS

def get_qualities (link: str) -> dict:
    video_qualities = []
    audio_qualities = []
    
    try:
        yt_vid = yt(link)
        vid_streams = yt_vid.streams.filter(mime_type="video/mp4")
        aud_streams = yt_vid.streams.filter(type="audio")

        for stream in vid_streams:
            if str(stream.resolution) not in video_qualities:
                video_qualities.append(str(stream.resolution))

        for stream in aud_streams:
            if str(stream.abr) not in audio_qualities:
                audio_qualities.append(str(stream.abr))


        return {
            "audio_qualities": audio_qualities,
            "video_qualities": video_qualities
        }
    except (InvalidYoutubeLinkError, AgeRestrictedError):
        with YoutubeDL(YOUTUBE_DL_OPTIONS) as ydl:
            video = ydl.extract_info(link, download=False)
            for stream in video['formats']:
                if stream.get('resolution') is not None and stream.get('resolution') != 'audio only' and stream.get('resolution') not in video_qualities:
                    video_qualities.append(stream["resolution"])
                if stream.get('abr') is not None and stream.get('abr') != 0 and stream.get('abr') not in audio_qualities:
                    audio_qualities.append(str(stream['abr']) + "kbps")
        
        return {
            "audio_qualities": audio_qualities,
            "video_qualities": video_qualities
        }
