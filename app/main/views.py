from app import login_manager
from app.main import main
from app.main.forms import LoginForm
from app.models import MESSAGES, users, User, Session
from flask import render_template, redirect, url_for, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from datetime import datetime
from .. import db

@login_manager.user_loader
def user_loader(email):
    print('user_loader')
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized access!!!'


@main.route('/')
def index():
    return render_template('index.html', msg=MESSAGES['default'])


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.user.data
        if form.pwd.data == users[username]['pw']:
            user = User()
            user.id = username
            login_user(user)

            # creates new row at sessions table
            new_session = Session(username=username, begin=datetime.now())
            db.session.add(new_session)
            db.session.commit()
            session['session_id'] = new_session.id

            return redirect(url_for('main.private'))
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    logout_user()

    # updates de end column
    current_session = Session.query.filter_by(id=session['session_id']).first()
    assert isinstance(current_session, Session)
    current_session.end = datetime.now()
    db.session.add(current_session)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/private')
@login_required
def private():
    return render_template('private.html', user=current_user.id)


@main.route('/show/<key>')
def get_message(key):
    return MESSAGES.get(key) or "%s not found!" % key


@main.route('/add/<key>/<message>')
def add_or_update_message(key, message):
    MESSAGES[key] = message
    return "%s Added/Updated" % key
