from flask import session ,render_template, redirect, send_file, request, Blueprint
from ytd_helper.static_links import StaticLinks

get_miltimedia_page = Blueprint('get_multimedia_page', __name__)

@get_miltimedia_page.route("/get")
def file_get():
    if ("yt_link" in session.keys()):
        try:
            return send_file(session['out_file'], as_attachment=True)
        except FileNotFoundError as e:
            return render_template("link_expired.html", links=StaticLinks)
        except Exception as e:
            return render_template("went_wrong.html", exception=e, links=StaticLinks)
    else:
        return redirect("/home")

@get_miltimedia_page.route("/get_aud")
def file_get_aud():
    if ("yt_link" in session.keys()):
        try:
            print(session['out_file'])
            return send_file(session['out_file'], as_attachment=True)
        except FileNotFoundError as e:
            return render_template("link_expired.html", links=StaticLinks)
        except Exception as e:
            return render_template("went_wrong.html", exception=e, links=StaticLinks)
    else:
        return redirect("/home")

@get_miltimedia_page.route("/download/path", methods=['GET'])
def download_from_link():
    try:
        return send_file(request.args.get('file_name'), as_attachment=True)
    except FileNotFoundError:
        return {'status': 404, 'description': "link expired!"}, 404
