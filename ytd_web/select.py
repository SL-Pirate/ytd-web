from flask import request, session, render_template,redirect, url_for, Blueprint
from ytd_helper.helper import Helper
from pytube.exceptions import RegexMatchError

select_page = Blueprint('select_page', __name__)

@select_page.route("/select", methods=["GET"])
def select():
    if (request.args.get("link") != None and request.args.get("link") != ""):
        session["yt_link"] = request.args.get("link")
        try:
            session['video'] = Helper(session).downloader(session)
            return render_template("select.html", vid_tit=session['video'][0], vid_img=session['video'][1], buttons=session['video'][2], buttons_aud=session['video'][3])
        except RegexMatchError:
            # session['q'] = session['yt_link']
            return redirect(url_for("browse", q=session["yt_link"]))
        except Exception as e:
            return render_template("went_wrong.html", exception=e)
            
    else:
        return redirect("/main")