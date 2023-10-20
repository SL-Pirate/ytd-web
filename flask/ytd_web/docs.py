from flask import Blueprint, render_template
from ytd_helper.static_links import StaticLinks

docs_page = Blueprint('docs_page', __name__)

@docs_page.route('/api_doc')
def api_doc():
    return render_template('api_doc.html', links=StaticLinks)
