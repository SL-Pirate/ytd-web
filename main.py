#!/usr/bin/env python

from flask import Flask
from ytd_helper import secret_key
from ytd_helper.static_links import StaticLinks

from ytd_web.home import home_page
from ytd_web.search import search_page
from ytd_web.browse import browse_page
from ytd_web.select import select_page
from ytd_web.multimedia import multimedia_page
from ytd_web.get_mulimedia import get_miltimedia_page
from ytd_web.download import download_page
from ytd_web.error import error_page

app = Flask(__name__)
StaticLinks(app.app_context())
app.register_blueprint(home_page)
app.register_blueprint(search_page)
app.register_blueprint(browse_page)
app.register_blueprint(select_page)
app.register_blueprint(multimedia_page)
app.register_blueprint(get_miltimedia_page)
app.register_blueprint(download_page)
app.register_blueprint(error_page)
app.secret_key = secret_key

# for testing purposes
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
