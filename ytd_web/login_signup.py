from flask import Blueprint, redirect, render_template, request
from db.user import User
from db.api_user import ApiUser
from ytd_helper.static_links import StaticLinks

login_signup_page = Blueprint('login_signup_page', __name__)

@login_signup_page.route('/login')
def login():
    return render_template('login.html')

@login_signup_page.route('/login_auth', methods=['POST'])
def authenticate():
    email = request.form.get('email')
    pw = request.form.get('password')

    user = User.login(email, pw)

    if (user != None):
        api_user = ApiUser.getUserFromUid(user.get_uid())
        if api_user == None:
            print(user)
            print(user.get_uid())
            api_user = ApiUser(user.get_uid())
            api_user.add_to_db()
        return render_template('dashboard.html', user=user, api_user=api_user)
    else:
        return render_template('login_failed.html', links=StaticLinks)


@login_signup_page.route('/signup')
def signup():
    return render_template("signup.html")

@login_signup_page.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = None

    pw = request.form.get('password')
    cnfrm_pw = request.form.get('confirm_password')

    if (pw == cnfrm_pw):
        password = pw

    else:
        return redirect('/signup')
    
    user = User(username, password, email)
    result = user.register()

    if result[0]:
        return render_template('signup_successful.html', links=StaticLinks)
    else:
        return render_template('signup_failed.html', links=StaticLinks, error_code=result[1]) 
