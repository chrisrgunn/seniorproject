from app import db
from models.exchange import Exchange

class TradeRate(db.Document):
    price = db.FloatField()
    date = db.DateTimeField()
    exchange = db.DocumentField(Exchange)

