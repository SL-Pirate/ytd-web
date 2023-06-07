from flask import Blueprint, request
from db.user import ApiUser

register_user = Blueprint('register_user', __name__)

@register_user.route('/register', methods=['GET', 'POST'])
def register():
    """
        request
        {
            "first_name": "First Name",
            "last_name": "Last Name",
            "username": "username"
        }

        response
        {
            "status": 200,
            "api_key": "Api Key"
        }
    """

    for item in ("first_name", "last_name", "username"):
        if item not in request.args.keys():
            return {'status': 416, 'request': request.args, "description": f"missing key: {item}"}, 416

    try:
        user = ApiUser(
            request.args.get('username'),
            first_name = request.args.get('first_name'),
            last_name = request.args.get('last_name')    
        )

        return {'status': 200, 'api_key': user.get_api_key()}
    
    except Exception as e:
        return {'status': 400, 'description': str(e)}, 400