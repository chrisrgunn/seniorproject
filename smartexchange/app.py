from flask import Flask, render_template, flash, redirect, request, url_for, session, make_response
from flask_mongoalchemy import MongoAlchemy
from forex_python.converter import CurrencyRates

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'mysecret'
db = MongoAlchemy(app)
salt = app.config['SALT']

# Model imports go here

from models.user import User
from models.exchange import Exchange
from models.trade_rate import TradeRate
from models.prediction import Prediction

# View imports go here

from views import homepage, logout, new_prediction, currency_tracker