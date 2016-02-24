from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional


class LoginForm(Form):
    user = StringField('Utilizador', validators=[DataRequired()])
    pwd = PasswordField('Palavra-passe', validators=[DataRequired()])
    task = StringField('Task', validators=[DataRequired()])
#    cat = SelectField('category', choices=[(1,'one'),(2,'two')], validators=[Optional()])
    submit = SubmitField('Submit')