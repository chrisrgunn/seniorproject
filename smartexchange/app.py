from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_mongoalchemy import MongoAlchemy
from forex_python.converter import CurrencyRates

app = Flask(__name__)
app.config.from_object('config')
db = MongoAlchemy(app)
salt = app.config['SALT']

# Model imports go here

from models.user import User

# View imports go here

from views import homepage, logout, new_prediction, currency_tracker