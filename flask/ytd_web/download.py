from flask import session, render_template, redirect, Blueprint
from ytd_helper import keep_time
from ytd_helper.helper import Helper
from ytd_helper.error import *
from ytd_helper.static_links import StaticLinks

download_page = Blueprint('download_page', __name__)

@download_page.route("/download")
def export():
    if ("yt_link" in session.keys()):
        try:
            Helper(session).process_video()
            return render_template("get_file.html", file_link=StaticLinks.file_get(), keep_time=keep_time, links=StaticLinks)
        except VideoProcessingFailureException as e:
            return render_template("went_wrong.html", exception=e, links=StaticLinks)
        except AttributeError:
            return redirect(StaticLinks.error())
    else:
        return redirect("/home")
    
@download_page.route("/download_aud")
def export_aud():
    if ("yt_link" in session.keys()):
        try:
            Helper(session).process_audio()
            return render_template("get_file.html", file_link=StaticLinks.file_get_aud(), keep_time=keep_time, links=StaticLinks)
        except AudioProcessingFailureException as e:
            return redirect(StaticLinks.error())
    else:
        return redirect("/home")
        
