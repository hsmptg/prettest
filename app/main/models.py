from flask.ext.login import UserMixin

MESSAGES = {
    'default': 'Hello to the World of Flask!',
}

users = {'hsmptg': {'pw': 'prettl'},
         'admin': {'pw': 'admin'}}

class User(UserMixin):
    pass