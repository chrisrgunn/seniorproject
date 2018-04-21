from app import db

class Exchange(db.Document):
    currency_from = db.StringField()
    currency_to = db.StringField()
