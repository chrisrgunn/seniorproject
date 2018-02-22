from app import db

class User(db.Document):
    name = db.StringField()
    username = db.StringField()
    email = db.StringField()
    password = db.StringField()
    authenticated = db.BoolField(default=False)
    avatar_image_reference = db.StringField(default=None)

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self, new_name, new_username, new_email, new_avatar_image_reference):
        if new_name:
            self.name = new_name
        if new_username:
            self.username = new_username
        if new_email:
            self.email = new_email
        if new_avatar_image_reference is not None and new_avatar_image_reference != "":
            self.avatar_image_reference = new_avatar_image_reference
        db.session.commit()

    def is_authenticated(self):
        # return true if user authenticated
        return self.authenticated

    def is_active(self):
        # true if user is an active user
        return True

    def is_anonymous(self):
        # true if anon user
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    # def is_admin(self):
    #     admin = Admin.query.filter_by(id=self.id).first()
    #     if admin is not None:
    #         return True
    #     else:
    #         return False

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()