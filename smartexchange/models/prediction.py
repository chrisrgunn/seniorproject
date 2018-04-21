from app import db
from models.exchange import Exchange
from models.user import User
from models.trade_rate import TradeRate

class Prediction(db.Document):
    date = db.DateTimeField()
    user = db.DocumentField(User)
    exchange = db.DocumentField(Exchange)

    trade_rates = db.ListField(db.DocumentField(TradeRate))

    num_days_in_past = db.IntField()
    num_days_in_future = db.IntField()
    seq_len = db.IntField()
    epochs = db.IntField()
    batch_size = db.IntField()

