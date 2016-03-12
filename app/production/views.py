# coding=utf-8

import time
from threading import Thread

from flask import render_template
from flask.ext.login import login_required

from app.production import production
from .. import socketio

from app.production.mcp3424 import MCP3424


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


@production.route('/production')
@login_required
def production():
    global thread_adc, exitADC

    print("begin adc thread")
    exitADC = False
    thread_adc = Thread(target=adc_proc)
    thread_adc.daemon = True
    thread_adc.start()

    return render_template('production.html')
