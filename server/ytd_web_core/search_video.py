from pytube import YouTube as yt
from pytube.exceptions import RegexMatchError as InvalidYoutubeLinkError
import requests
from ytd_web_core import Status, YOUTUBE_DL_OPTIONS
from yt_dlp.utils import DownloadError
from ytd_web_core.exceptions import InvalidLinkError
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from ytd_web_core.models import SearchResult
from configparser import ConfigParser
from ytd_web_core.util import get_url_from_video_id

_config = ConfigParser()
_config.read(".env")
_api_key = _config["googleApiKey"]["key"]

def get_channel_thumbnail_url(channel_ids: list[str]) -> dict:
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet&maxResults=10&key={_api_key}&type=video"
    for channel_id in channel_ids:
        url += f"&id={channel_id}"

    payload = {}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        channel_thumbnails: dict = dict()
        for channel in response.json()['items']:
            channel_thumbnails[channel['id']] = channel['snippet']['thumbnails']['default']['url']
        return channel_thumbnails
    else:
        return dict()

def search_video_from_url(url: str) -> list[SearchResult]:
    try:
        search_term = url
        video = yt(search_term)
        return [SearchResult(
            video_id=video.video_id,
            url=url,
            title=video.title,
            description=video.description,
            thumbnail_url=video.thumbnail_url,
            channel_name=video.channel_id,
            channel_thumbnail_url=get_channel_thumbnail_url([video.channel_id])
        )]
    except Exception:
        with YoutubeDL(YOUTUBE_DL_OPTIONS) as ydl:
            try:
                video = ydl.extract_info(url, download=False)
                return [SearchResult(
                    source="other",
                    url=url,
                    video_id=video.get('id'),
                    title=video.get('title'),
                    description=video.get('description'),
                    thumbnail_url=video.get('thumbnail'),
                    channel_name=video.get('uploader')
                )]
            except DownloadError:
                raise InvalidLinkError()

def search(request) -> list[SearchResult]:
    try:
        search_term = request.GET.get('keyword', '')
        return search_video_from_url(search_term)
    
    except InvalidLinkError:
        url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q={search_term}&key={_api_key}&type=video"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            search_results = response.json()['items']
            search_result_objs = list()

            # obtaining channel thumbnail urls
            channel_ids: list[str] = list()
            for search_result in search_results:
                channel_ids.append(search_result['snippet']['channelId'])
            channel_thumbnails: dict = get_channel_thumbnail_url(channel_ids)

            for search_result in search_results:
                search_result_objs.append(
                    SearchResult(
                        video_id=search_result['id']['videoId'], 
                        url=get_url_from_video_id(search_result['id']['videoId']),
                        title=search_result['snippet']['title'],
                        description=search_result['snippet']['description'],
                        thumbnail_url=search_result['snippet']['thumbnails']['high']['url'],
                        channel_name=search_result['snippet']['channelTitle'],
                        channel_thumbnail_url=channel_thumbnails.get(search_result['snippet']['channelId'])
                    )
                )
            return search_result_objs
        
        else:
            return [SearchResult(status=Status.FAILURE)]
