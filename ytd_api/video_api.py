from flask import Blueprint, request,session, url_for
from ytd_helper import api_key, api_server_root, keep_time
from ytd_helper.helper import Helper
from ytd_helper.static_links import StaticLinks
from pytube.exceptions import RegexMatchError
import os

vid_api = Blueprint('video_api', __name__)

# _____________________ API FOR DIRECT VIDEO DOWNLOADING WITH LINK _________________________
@vid_api.route("/get_video", methods=['POST'])
def getVideo():
    '''
        request
        {
            "key": "api key",
            "video_link": "video link",
            "resolution": "resolution"
        }

        response
        {
            "status": status_code,
            "title": "video title",
            "resolution": "video resolution",
            "format": "video format"
            "download_link": "download_link"
        }
    '''
    for item in ("key", "video_link", "resolution"):
        if item not in request.args.keys():
            return {'status': 416, 'request': request.args, "description": f"missing key: {item}"}, 416

    if request.args.get('key') == api_key:
        try:
            dl = Helper(session).downloader(link=request.args.get("video_link"), resolution=request.args.get("resolution"))
            session["video"] = dl
            try:
                Helper(session).process_video()
                out_file = session['out_file']
                print(out_file)
                pre, ext = os.path.splitext(out_file)
                return {
                    'status': 200, 
                    'title': dl[0], 
                    'resolution': request.args.get('resolution'), 
                    'format': ext, 
                    'download_link': api_server_root + StaticLinks.download_from_link(out_file), 
                    "link expire duration": str(keep_time) + " minutes"
                }
            except AttributeError:
                return {'status': 404, 'description': "Resolution " + request.args.get("resolution") + " not found"}
            except Exception as e:
                # print(traceback.format_exc())
                return {'status': 500,"description": str(e)}, 500
        except RegexMatchError:
            return {'status': 404, 'description': "Invalid URL"}, 404

    else:
        return {'status': 401,"description": "Invalid API Key"}, 401
