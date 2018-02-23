from app import db

class User(db.Document):
    name = db.StringField()
    username = db.StringField()
    email = db.StringField()
    password = db.StringField()
    authenticated = db.BoolField(default=False)
    avatar_image_reference = db.StringField(default=None)