from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_mongoalchemy import MongoAlchemy
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config.from_object('config')
# mongo = PyMongo(app)
db = MongoAlchemy(app)
salt = app.config['SALT']
from models.test import Test
from models.user import User

from views import homepage

# def home_page():
#     online_users = mongo.db.users.find({'online': True})
#     return render_template('user.html',
#         online_users=online_users)

@app.route('/login', methods=['POST'])
def login():
    login_user = User.query.filter(User.username==request.form['username']).first()

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            flash("You have been signed in!", "success")
            return render_template("home.html")
    flash('Invalid username/password combination', "danger")
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['form-btn'] == "SIGN IN":
            login_user = User.query.filter(User.username == request.form['username/email']).first()
            if login_user:
                if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user.password.encode('utf-8')) == login_user.password.encode('utf-8'):
                    session['username'] = request.form['username/email']
                    flash("Sign in successful!", "success")
                    return redirect(url_for("index"))
                flash("Invalid password!", "danger")
                return redirect(url_for("index"))
            return 'Invalid username'
        elif request.form['form-btn'] == "SIGN UP":
            if User.query.filter(User.username == request.form['username']).first() is not None:
                return "username already taken"
            if User.query.filter(User.email == request.form['email']).first() is not None:
                return "email already taken"
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            new_user = User(name=request.form['name'], username=request.form['username'], password=hashpass, email=request.form['email'])
            new_user.save()
            return "You have made an account successfully!"
    return render_template('home.html')

@app.route('/exists/<username>/<email>')
def exists(username, email):
    return User.exists(username, email)
    # user = User.query.filter(User.username==username).first()
    # if user is None:
    #     return 'no user found'
    # return user.username;

@app.route('/user/<username>')
def user_profile(username):
    user = mongo.db.users.find_one_or_404({'_id': username})
    return render_template('user.html',
        user=user)

@app.route('/add/<username>/<email>')
def add(username, email):
    user = User(username=username, email=email, name='test', password='test')
    user.save()
    # user = mongo.db.users
    # user.insert({'name' : username, 'eye_color':'blue'})
    return 'Added User!'

@app.route('/logout')
def logout():
    session['username'] = None
    return render_template('home.html')
