from flask import Blueprint

from ytd_api.audio_api import audio_api
from ytd_api.video_api import vid_api
from ytd_api.qual_api import qual_api

endpoints: list[Blueprint] = [audio_api, vid_api, qual_api]
