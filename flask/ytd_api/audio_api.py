from flask import Blueprint, request, session
from ytd_helper import api_server_root, keep_time
from ytd_helper.helper import Helper
from ytd_helper.static_links import StaticLinks
from db.api_user import ApiUser
from pytube.exceptions import RegexMatchError
import os

audio_api = Blueprint('audio_api', __name__)

# _____________________ API FOR DIRECT VIDEO DOWNLOADING WITH LINK _________________________
@audio_api.route("/get_audio", methods=['POST'])
def getAudio():
    '''
        request
        {
            "key": "api key",
            "video_link": "video link",
            "quality": "quality"
        }

        response 200
        {
            "status": status_code,
            "title": "Audio file title",
            "quality": "Audio quality",
            "format": "audio format"
            "download_link": "download_link"
        }
        response 400
        {
            "status": status_code,
            "description": "reason for faliure"
        }
    '''
    for item in ("key", "video_link", "quality"):
        if item not in request.args.keys():
            return {'status': 416, 'request': request.args, "description": f"missing key: {item}"}, 416

    if ApiUser.validate_api_key(request.args.get('key')):
        try:
            dl = Helper(session).downloader(link=request.args.get("video_link"), quality=request.args.get("quality"))
            session["video"] = dl
            try:
                Helper(session).process_audio()
                out_file = session['out_file']
                pre, ext = os.path.splitext(out_file)
                return {
                    'status': 200, 
                    'title': dl[0], 
                    'quality': request.args.get('quality'), 
                    'format': ext, 
                    'download_link': api_server_root + StaticLinks.download_from_link(out_file), 
                    'link expire duration': str(keep_time) + " minutes"
                }
            except AttributeError:
                return {'status': 404, 'description': "quality " + request.args.get("quality") + " not found"}
            except Exception as e:
                return {'status': 500,"description": str(e)}, 500
        except RegexMatchError:
            return {'status': 404, 'description': "Invalid URL"}, 404

    else:
        return {'status': 401,"description": "Invalid API Key"}, 401
