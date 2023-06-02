from flask import request, session, redirect, url_for, Blueprint
from pytube import YouTube as yt
from pytube.exceptions import RegexMatchError

search_page = Blueprint('search_page', __name__)

@search_page.route("/search", methods=["GET"])
def search():
    print(__name__)
    if (request.args.get("link") != None and request.args.get("link") != ""):
        yt_link = request.args.get("link")
        session["yt_link"] = yt_link
        try:
            yt(yt_link)
            return redirect(url_for("select", link=yt_link))
        except RegexMatchError:
            return redirect(url_for("browse", q=yt_link))
    else:
        return redirect("/home")