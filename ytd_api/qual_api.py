from flask import Blueprint, request, session
from ytd_helper import api_key
from ytd_helper.helper import Helper
from db.user import ApiUser
from pytube.exceptions import RegexMatchError

qual_api = Blueprint('qual_api', __name__)

# _____________________ API FOR FETCHING AVAILABLE RESOLUTIONS/QUALITIES WITH LINK _________________________
@qual_api.route("/get_qual", methods=['POST'])
def getResolution():
    '''
        request
        {
            "key": "api key",
            "video_link": "video link"
        }

        response
        {
            "status": status_code,
            "title": "video title",
            "available_video_resolutions": ["res1", "res2],
            "available_audio_qualities": ["qual1", "qual2"]
        }
    '''
    for item in ("key", "video_link"):
        if item not in request.args.keys():
            return {'status': 416, 'request': request.args, "description": f"missing key: {item}"}, 416

    if ApiUser.validate_api_key(request.args.get('key')):
        try:
            dl = Helper(session).downloader(link=request.args.get("video_link"))
            session["video"] = dl

            return {'status': 200, 'title': dl[0], 'available_video_resolutions': dl[2], 'available_audio_resolutions': dl[3]}
        except RegexMatchError:
            return {'status': 404, 'description': "Invalid URL"}, 404

    else:
        return {'status': 401,"description": "Invalid API Key"}, 401
