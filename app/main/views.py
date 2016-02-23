# coding=utf-8
from app import login_manager
from app.main import main
from app.main.forms import LoginForm
from app.models import User, Task
from flask import render_template, redirect, url_for, session, request, flash
from flask.ext.login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from .. import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Acesso n&atilde;o autorizado!!!'


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.user.data
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash(u"O utilizador não existe!")
        elif not check_password_hash(user.password_hash, form.pwd.data):
            flash("A palavra-passe está incorreta!")
        else:
            login_user(user)

            # creates new row at Task table
            new_task = Task(username=username, begin=datetime.now(),
                            task=form.task.data)
            db.session.add(new_task)
            db.session.commit()
            session['task_id'] = new_task.id

            if form.task.data == "production":
                return redirect(url_for('main.production'))
            elif form.task.data == "maintenance":
                return redirect(url_for('main.maintenance'))
            elif form.task.data == "setup":
                return redirect(url_for('main.setup'))
            elif form.task.data == "data":
                return redirect(url_for('main.data'))
    else:
        if request.method == "POST":
            flash("Preencha todos os campos!")

    return render_template('index.html', form=form,
                           rpi=(request.remote_addr == "127.0.0.1"))


@main.route('/admyn')
def create_admin():
    new_user = User(username="admin", password_hash="xxx")
    new_user.password_hash = generate_password_hash("admin")
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/production')
@login_required
def production():
    return render_template('production.html')


@main.route('/maintenance')
@login_required
def maintenance():
    return render_template('maintenance.html')


@main.route('/setup')
@login_required
def setup():
    return render_template('setup.html')


@main.route('/data')
@login_required
def data():
    return render_template('data.html')


@main.route('/logout')
def logout():
    logout_user()

    # updates de end column
    current_task = Task.query.filter_by(id=session['task_id']).first()
    assert isinstance(current_task, Task)
    current_task.end = datetime.now()
    db.session.add(current_task)
    db.session.commit()

    return redirect(url_for('main.index'))
