from flask import session, request, render_template, redirect, Blueprint

multimedia_page = Blueprint('multimedia_page', __name__)

@multimedia_page.route("/video")
def download_vid():
    if ("yt_link" in session.keys()):
        session['reso'] = request.args.get("reso")
        return render_template("downloading.html")
    else:
        return redirect("/home")
    
@multimedia_page.route("/audio")
def download_aud():
    if ("yt_link" in session.keys()):
        session['qual'] = request.args.get("qual")
        return render_template("downloading_aud.html")
    else:
        return redirect("/home")
