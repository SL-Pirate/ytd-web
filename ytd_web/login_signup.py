from flask import Blueprint, redirect, render_template, request, session
from db.user import User
from db.api_user import ApiUser
from ytd_helper.static_links import StaticLinks

login_signup_page = Blueprint('login_signup_page', __name__)

@login_signup_page.route('/login')
def login():
    return render_template('login.html', links=StaticLinks)

@login_signup_page.route('/login_auth', methods=['POST', 'GET'])
def authenticate():
    email = request.form.get('email')
    pw = request.form.get('password')

    user = User.login(email, pw)
    if (user == None):
        return render_template('login_failed.html', links=StaticLinks)
    else:
        logout_method()
        session['email'] = email
        session['password'] = pw
        return redirect(StaticLinks.dashboard())
    
@login_signup_page.route('/signup')
def signup():
    return render_template("signup.html", links=StaticLinks)

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

@login_signup_page.route('/logout')
def logout():
    logout_method()
    return render_template('logout_successful.html', links=StaticLinks)

def logout_method():
    if (session.get('email') != None and session.get('password') != None):
        session['email'] = None
        session['password'] = None