from flask import Blueprint, send_file, request

get_multimedia_via_api = Blueprint('get_multimedia_via_api', __name__)

@get_multimedia_via_api.route("/download/path", methods=['GET'])
def download_from_link():
    protected_files = ["secrets.key"]
    for protected_file in protected_files:
        if protected_file in request.args.get('file_name'):
            return {'status': 403, 'description': "Illegal file name!"}, 403
    try:
        return send_file(request.args.get('file_name'), as_attachment=True)
    except FileNotFoundError:
        return {'status': 404, 'description': "link expired!"}, 404
