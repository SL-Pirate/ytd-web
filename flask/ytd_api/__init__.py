from flask import Blueprint

from ytd_api.audio_api import audio_api
from ytd_api.video_api import vid_api
from ytd_api.qual_api import qual_api
from ytd_api.get_multimedia import get_multimedia_via_api
# from ytd_api.create_user import register_user

endpoints: list[Blueprint] = [audio_api, vid_api, qual_api, get_multimedia_via_api]
