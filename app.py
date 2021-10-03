import flask 
from flask import Flask, session, request, render_template, abort, redirect, url_for
#from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import database
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from urllib.parse import urlparse, urljoin


app = Flask(__name__)
#auth = HTTPBasicAuth()
login_manager = LoginManager()


login_manager.init_app(app)


users = {
    "melba": generate_password_hash("melba"),
    "freddie123": generate_password_hash("freddie123"),
    "chucky": generate_password_hash("chucky"),
}

app.secret_key = "kdjgabvsega\f"




@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User():
    def __init__(self, username):
        self.username = username

    def is_active(self):
        return True

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.email
    
    @classmethod
    def get(cls, username):
        return User(username)

@app.route('/login', methods=['GET', 'POST'])
def login():
     # Here we use a class of some kind to represent and validate our
     # client-side form data. For example, WTForms is a library that will
     # handle this for us, and we use a custom LoginForm to validate.

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and \
            check_password_hash(users.get(username), password):
             
         # user should be an instance of your `User` class
            user= current_user
        login_user(user)
        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
         # is_safe_url should check if the url is safe for redirects.
         # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('feed'))
    return flask.render_template('login.html', form=form)
# @auth.verify_password
# def verify_password(username, password):
#      if username in users and \
#              check_password_hash(users.get(username), password):
#          return username

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
    
@app.route("/")
def splash():
    #  if auth.current_user():
    #      return redirect('feed')
    #  else:
        return render_template('splash.html')

@app.route("/feed")
@login_required
def feed():
    dogs = database.get_all_facts()
    cus = username
    print(username)
    posts = database.get_one_dog(user)
    picture = posts[0]['Picture']
    name= posts[0]['Name']
    return render_template('feed.html', dogs=dogs, cus=cus, name=name, profilepic = picture)

@app.route('/delete/<string:post_id>')
@login_required
def delete(post_id):
    database.delete_post(post_id)
    return redirect(url_for('feed'))

@app.route("/profile/<string:dog_id>")
@login_required
def profile(dog_id):
    posts = database.get_one_dog(dog_id)
    username = posts[0]['Handle']
    picture = posts[0]['Picture']
    bio = posts[0]['Bio']
    return render_template('profile.html', title = dog_id, posts=posts, username=username, picture=picture, bio=bio)

@app.route('/create', methods = ['POST'])
@login_required
def create():
    post_content=request.form['post-content']
    handle=auth.current_user()
    database.insert_post(handle, post_content)
    dogs = database.get_all_facts()
    return redirect(url_for('feed'))

# @app.route("/logout")
# def logout():
#     return render_template('splash.html'), 401

@app.route("/logout")
@login_required
def logout():
     logout_user()
     return redirect(somewhere)
  