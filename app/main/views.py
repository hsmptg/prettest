from flask import render_template, session, redirect, url_for
from app.main.models import MESSAGES
from app.main.forms import LoginForm
from app.main import main


@main.route('/')
def index():
    return render_template('index.html', msg=MESSAGES['default'])


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['user'] = form.user.data
        return redirect(url_for('main.private'))
    return render_template('login.html', form=form)


@main.route('/private')
def private():
    return render_template('private.html')


@main.route('/show/<key>')
def get_message(key):
    return MESSAGES.get(key) or "%s not found!" % key


@main.route('/add/<key>/<message>')
def add_or_update_message(key, message):
    MESSAGES[key] = message
    return "%s Added/Updated" % key
