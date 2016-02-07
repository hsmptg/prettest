from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    user = StringField('Username?', validators=[DataRequired()])
    pwd = PasswordField('Password?', validators=[DataRequired()])
    submit = SubmitField('Submit')