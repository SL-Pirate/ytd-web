from flask import session, render_template, redirect, Blueprint

error_page = Blueprint('error_page', __name__)

@error_page.route("/Error")
def not_found():
    if ("yt_link" in session.keys()):
        return render_template("error.html")
    else: 
        return redirect("/home")