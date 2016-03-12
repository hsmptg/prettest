# coding=utf-8

import platform
import time
from datetime import datetime
from threading import Thread

from flask import render_template, redirect, url_for, session, request, flash
from flask.ext.login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app import login_manager
from app.main import main
from app.main.forms import LoginForm
from app.models import User, Task
from .. import db, socketio

if platform.uname()[4][0:3] == "arm":
    import rc522
else:
    import rc522_alt as rc522
from app.main.mcp3424 import MCP3424


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return unicode("Acesso não autorizado!!!", "utf8")


thread_rfid = None
exitRFID = False
MIFAREReader = rc522.MFRC522()


def rfid_proc(app):
    global MIFAREReader, exitRFID

    while not exitRFID:
        time.sleep(1)
        uid = MIFAREReader.MRFC522_readUID()
        if uid is not None:
            print("Card " + uid)
            with app.app_context():
                user = User.query.filter_by(rfid=uid).first()
                if user is None:
                    msg = {'user': "", "rfid": uid}
                else:
                    msg = {'user': user.username, "rfid": uid}
            print(msg)
            socketio.emit('rfid', msg, namespace='/rfid')

    print('exit thread')


@main.route('/', methods=['GET', 'POST'])
def index():
    global thread_rfid, exitRFID

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.user.data
            user = User.query.filter_by(username=username).first()

            if user is None or form.rfid.data == "":
                flash(unicode("O utilizador não existe!", "utf8"))
            elif form.rfid.data == "" and not check_password_hash(user.password_hash, form.pwd.data):
                flash(unicode("A palavra-passe está incorreta!", "utf8"))
            else:
                login_user(user)

                # creates new row at Task table
                new_task = Task(username=username, begin=datetime.now(),
                                task=form.task.data)
                db.session.add(new_task)
                db.session.commit()
                session['task_id'] = new_task.id

                if request.remote_addr == "127.0.0.1":
                    exitRFID = True

                if form.task.data == "production":
                    return redirect(url_for('main.production'))
                elif form.task.data == "maintenance":
                    return redirect(url_for('main.maintenance'))
                elif form.task.data == "setup":
                    return redirect(url_for('main.setup'))
                elif form.task.data == "data":
                    return redirect(url_for('main.data'))
        else:
            flash("Preencha todos os campos!")
    else:
        if request.remote_addr == "127.0.0.1":
            print("begin thread")
            exitRFID = False
            # thread_rfid = Thread(target=rfid_proc,
            #                      args=(current_app._get_current_object(),))
            # thread_rfid.daemon = True
            # thread_rfid.start()
    return render_template('index.html', form=form,
                           rpi=(request.remote_addr == "127.0.0.1"))


@main.route('/admyn')
def create_admin():
    new_user = User(username="admin")
    new_user.password_hash = generate_password_hash("admin")
    new_user.rfid = "EC:A4:F9:34"
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.index'))


thread_adc = None
exitADC = False
adc = MCP3424()


def adc_proc():
    global adc, exitADC

    while not exitADC:
        time.sleep(.1)
        dat = adc.getData()
        print(dat)
        socketio.emit('newData', {'data': dat}, namespace='/adc')

    print('exit adc thread')


@main.route('/production')
@login_required
def production():
    global thread_adc, exitADC

    print("begin adc thread")
    exitADC = False
    thread_adc = Thread(target=adc_proc)
    thread_adc.daemon = True
    thread_adc.start()

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

