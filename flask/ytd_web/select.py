from flask import request, session, render_template,redirect, Blueprint
from ytd_helper.helper import Helper
from ytd_helper.static_links import StaticLinks
from pytube.exceptions import RegexMatchError

select_page = Blueprint('select_page', __name__)

@select_page.route("/select", methods=["GET"])
def select():
    if (request.args.get("link") != None and request.args.get("link") != ""):
        session["yt_link"] = request.args.get("link")
        try:
            session['video'] = Helper(session).downloader()
            return render_template("select.html", vid_tit=session['video'][0], vid_img=session['video'][1], buttons=session['video'][2], buttons_aud=session['video'][3], links=StaticLinks)
        except RegexMatchError:
            return redirect(StaticLinks.browse(session['yt_link']))
        except Exception as e:
            return render_template("went_wrong.html", exception=e, links=StaticLinks)
            
    else:
        return redirect("/main")