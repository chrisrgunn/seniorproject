from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_mongoalchemy import MongoAlchemy
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('config')
# mongo = PyMongo(app)
db = MongoAlchemy(app)

from models.test import Test


from views import homepage

# def home_page():
#     online_users = mongo.db.users.find({'online': True})
#     return render_template('user.html',
#         online_users=online_users)


@app.route('/user/<username>')
def user_profile(username):
    user = mongo.db.users.find_one_or_404({'_id': username})
    return render_template('user.html',
        user=user)

@app.route('/add/<username>')
def add(username):
    test = Test(name=username)
    test.save()
    # user = mongo.db.users
    # user.insert({'name' : username, 'eye_color':'blue'})
    return 'Added User!'
