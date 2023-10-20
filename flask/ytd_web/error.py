from flask import session, render_template, redirect, Blueprint
from ytd_helper.static_links import StaticLinks

error_page = Blueprint('error_page', __name__)

@error_page.route("/error")
def not_found():
    if ("yt_link" in session.keys()):
        return render_template("error.html", links=StaticLinks)
    else: 
        return redirect("/home")