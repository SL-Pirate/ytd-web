from flask import Blueprint, session, render_template, redirect, request
from db.user import User
from db.api_user import ApiUser
from ytd_helper.static_links import StaticLinks

dashboard_page = Blueprint('dashboard_page', __name__)

@dashboard_page.route('/dashboard')
def dashboard():
    if (session.get('email') != None and session.get('password') != None):
        email = session['email']
        pw = session['password']
        user = User.login(email, pw)
        uid = user.get_uid()
        api_keys = ApiUser.getUserFromUid(uid)
        return render_template('dashboard.html', user=user, api_keys=api_keys, links=StaticLinks)
    else:
        return redirect(StaticLinks.login())
    
@dashboard_page.route('/gen_api_key', methods=['POST'])
def gen_api_key():
    uid = request.form.get('uid')
    ApiUser(uid).add_to_db()
    return redirect(StaticLinks.dashboard())

@dashboard_page.route('/del_api_key')
def del_api_key():
    api_key = request.args.get('api_key')
    ApiUser.del_api_key(api_key)
    return redirect(StaticLinks.dashboard())
