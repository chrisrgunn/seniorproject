from app import db

class Test(db.Document):
    name = db.StringField()