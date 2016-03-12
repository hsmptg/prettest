import os
from app import create_app, socketio
from flask.ext.script import Manager
import signal
import sys

exitFlag = False

def signal_handler(signal, frame):
    global exitFlag

    exitFlag = True
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def run():
    # nao da para especificar o host, port da linha de comando pelo script?
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)


if __name__ == '__main__':
    manager.run()
