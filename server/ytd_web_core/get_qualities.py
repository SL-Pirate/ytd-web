from pytube import YouTube as yt
from pytube.exceptions import AgeRestrictedError
from ytd_web_core.exceptions import AgeRestrictedVideoException

def get_qualities (link: str) -> dict:
    try:
        yt_vid = yt(link)
        vid_streams = yt_vid.streams.filter(mime_type="video/mp4")
        aud_streams = yt_vid.streams.filter(type="audio")
        
        video_qualities = []
        audio_qualities = []

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
    except AgeRestrictedError:
        raise AgeRestrictedVideoException
