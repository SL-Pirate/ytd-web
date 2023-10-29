from configparser import ConfigParser
from pytube import YouTube as yt
from pytube.exceptions import RegexMatchError as InvalidLinkError
import requests
from ytd_web_core import Status

config = ConfigParser()
config.read(".env")
_api_key = config["googleApiKey"]["key"]


class SearchResult:
    def __init__(
        self, 
        video_id: str = None,
        title: str = None, 
        thumbnail_url: str = None, 
        channel_name: str = None, 
        server_ip: str = None,
        status: Status = Status.SUCCESSFUL
    ) -> None:
        self._title = title
        self._video_id = video_id
        self._channel_name = channel_name
        self._status = status

        if (server_ip == None):
            self._thumbnail_url = thumbnail_url
        else:
            self._thumbnail_url = f"{server_ip}/proxy?url={thumbnail_url}"

    def get_channel_name(self):
        return self._channel_name
    
    def get_title(self):
        return self._title
    
    def get_thumbnail_url(self):
        return self._thumbnail_url
    
    def get_status(self):
        return self._status
    
    def get_video_id(self):
        return self._video_id
    
    def JsonSerialize(self):
        return {
            "video_id": self._video_id,
            "title": self._title,
            "thumbnail_url": self._thumbnail_url,
            "channel_name": self._channel_name
        }

def search(request) -> list[SearchResult]:
    server_ip = request.build_absolute_uri().split("/api")[0]
    try:
        search_term = request.GET.get('keyword', '');
        video = yt(search_term)
        return [SearchResult(
            video.video_id,
            video.title,
            video.thumbnail_url,
            video.channel_id,
            server_ip
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
            for search_result in search_results:
                search_result_objs.append(
                    SearchResult(
                        search_result['id']['videoId'], 
                        search_result['snippet']['title'],
                        search_result['snippet']['thumbnails']['high']['url'],
                        search_result['snippet']['channelTitle'],
                        server_ip
                    )
                )
            return search_result_objs
        
        else:
            return [SearchResult(status=Status.FAILURE)]
