from flask import session, render_template, redirect, Blueprint
from ytd_helper import keep_time
from ytd_helper.helper import Helper
from ytd_helper.error import *

download_page = Blueprint('download_page', __name__)

@download_page.route("/download")
def export():
    if ("yt_link" in session.keys()):
        try:
            Helper(session).process_video()
            return render_template("get_file.html", file_link="file_get", keep_time=keep_time)
        except VideoProcessingFailureException as e:
            return render_template("went_wrong.html", exception=e)
    else:
        return redirect("/home")
    
@download_page.route("/download_aud")
def export_aud():
    if ("yt_link" in session.keys()):
        try:
            Helper(session).process_audio()
            return render_template("get_file.html", file_link="file_get_aud", keep_time=keep_time)
        except AudioProcessingFailureException as e:
            return render_template("went_wrong.html", exception=e)
    else:
        return redirect("/home")
        
