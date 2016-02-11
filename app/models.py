from flask.ext.login import UserMixin
from . import db

MESSAGES = {
    'default': 'Hello to the World of Flask!',
}

users = {'hsmptg': {'pw': 'prettl'},
         'admin': {'pw': 'admin'}}

class User(UserMixin):
    pass

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    begin = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    def __repr__(self):
        pass
        #return '<User %r>' % self.username