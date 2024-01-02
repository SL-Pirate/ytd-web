from configparser import ConfigParser
from enum import Enum

config = ConfigParser()
config.read("server.cfg")
config = config["DEFAULT"]

keep_time: int = int(config['keep_time'])
max_vids: int = int(config['max_vids'])
cache_folder: str = config['cache_folder']

class Status(Enum):
    SUCCESSFUL = 1
    FAILURE = -1

YOUTUBE_DL_OPTIONS = {
    'quiet': True,
    'skip_download': True,
    'no_warnings': True
}
