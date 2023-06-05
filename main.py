#!/usr/bin/env python

from flask import Flask
from ytd_helper import secret_key
from ytd_helper.static_links import StaticLinks
from ytd_web import endpoints
from ytd_api import endpoints as api_endpoints

app = Flask(__name__)

StaticLinks(app.app_context())
for endpoint in endpoints:
    app.register_blueprint(endpoint)
for endpoint in api_endpoints:
    app.register_blueprint(endpoint)

app.secret_key = secret_key

# for testing purposes
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
