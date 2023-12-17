from configparser import ConfigParser
from pytube import YouTube as yt
from pytube.exceptions import RegexMatchError as InvalidLinkError
import requests
from ytd_web_core import Status

config = ConfigParser()
config.read(".env")
_api_key = config["googleApiKey"]["key"]
_server_ip = config["server"]["ip"]


class SearchResult:
    def __init__(
        self, 
        video_id: str = None,
        title: str = None, 
        description: str = None,
        thumbnail_url: str = None, 
        channel_name: str = None, 
        channel_thumbnail_url: str = None,
        status: Status = Status.SUCCESSFUL
    ) -> None:
        self._video_id = video_id
        self._title = title
        self._description = description
        self._channel_name = channel_name
        self._channel_thumbnail_url = channel_thumbnail_url
        self._status = status

        if (_server_ip == None):
            self._thumbnail_url = thumbnail_url
            self._channel_thumbnail_url = channel_thumbnail_url
        else:
            self._thumbnail_url = f"{_server_ip}/proxy?url={thumbnail_url}"
            self._channel_thumbnail_url = f"{_server_ip}/proxy?url={channel_thumbnail_url}"

    def get_video_id(self):
        return self._video_id
    
    def get_title(self):
        return self._title
    
    def get_description(self):
        return self._description
    
    def get_thumbnail_url(self):
        return self._thumbnail_url
    
    def get_channel_name(self):
        return self._channel_name
    
    def get_channel_thumbnail_url(self):
        return self._channel_thumbnail_url

    def get_status(self):
        return self._status
    
    
    def JsonSerialize(self):
        return {
            "video_id": self._video_id,
            "title": self._title,
            "edscription": self._description,
            "thumbnail_url": self._thumbnail_url,
            "channel_name": self._channel_name,
            "channel_thumbnail_url": self._channel_thumbnail_url
        }

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

def search(request) -> list[SearchResult]:
    try:
        search_term = request.GET.get('keyword', '')
        video = yt(search_term)
        return [SearchResult(
            video_id=video.video_id,
            title=video.title,
            description=video.description,
            thumbnail_url=video.thumbnail_url,
            channel_name=video.channel_id,
            channel_thumbnail_url=get_channel_thumbnail_url([video.channel_id])
        )]
    
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
