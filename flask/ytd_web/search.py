from flask import request, session, redirect, Blueprint
from pytube import YouTube as yt
from pytube.exceptions import RegexMatchError
from ytd_helper.static_links import StaticLinks

search_page = Blueprint('search_page', __name__)

@search_page.route("/search", methods=["GET"])
def search():
    if (request.args.get("link") != None and request.args.get("link") != ""):
        yt_link: str = request.args.get("link")
        session["yt_link"] = yt_link
        try:
            yt(yt_link)
            return redirect(StaticLinks.select(yt_link))
        except RegexMatchError:
            return redirect(StaticLinks.browse(yt_link))
    else:
        return redirect("/home")