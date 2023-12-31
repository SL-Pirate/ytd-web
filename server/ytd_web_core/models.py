from collections.abc import Iterable
from django.db import models
from ytd_web_core import keep_time
from ytd_web_core.celery import clean_func
from sequences import get_next_value
from configparser import ConfigParser
from ytd_web_core import Status

_config = ConfigParser()
_config.read(".env")
_server_ip = _config["server"]["ip"]

class Downloadable(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.TextField()
    name = models.TextField()
    folder = models.TextField()
    expiration_period = models.IntegerField(default=keep_time)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.id = get_next_value("downloadable_id", reset_value=2000000000);
        super().save(force_insert, force_update, using, update_fields)


    def initInvalidation(self) -> None:
        clean_func.delay(self.folder, self.id)

class SearchResult:
    def __init__(
        self, 
        source: str = "youtube",
        url: str = None,
        video_id: str = None,
        title: str = None, 
        description: str = None,
        thumbnail_url: str = None, 
        channel_name: str = None, 
        channel_thumbnail_url: str = None,
        status: Status = Status.SUCCESSFUL
    ) -> None:
        self._source = source
        self._url = url
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
            self._thumbnail_url = f"{_server_ip}/proxy?url={thumbnail_url}" if thumbnail_url is not None else None
            self._channel_thumbnail_url = f"{_server_ip}/proxy?url={channel_thumbnail_url}" if channel_thumbnail_url is not None else None

    def get_source(self):
        return self._source
    
    def get_url(self):
        return self._url

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
            "source": self._source,
            "url": self._url,
            "video_id": self._video_id,
            "title": self._title,
            "description": self._description,
            "thumbnail_url": self._thumbnail_url,
            "channel_name": self._channel_name,
            "channel_thumbnail_url": self._channel_thumbnail_url
        }

