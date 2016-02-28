from flask.ext.login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    rfid = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
#    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        pass


class Task(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    task = db.Column(db.String(64))
    begin = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    def __repr__(self):
        pass
        #return '<User %r>' % self.username