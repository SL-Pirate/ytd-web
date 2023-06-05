from flask import render_template, Blueprint
from ytd_helper.static_links import StaticLinks

home_page = Blueprint('home_page', __name__)

# _____________________HOME PAGE___________________________
@home_page.route("/", methods=["GET"])
@home_page.route("/main", methods=["GET"])
@home_page.route("/home", methods=["GET"])
def home():
    print(__name__)
    return render_template("index.html", links=StaticLinks)
