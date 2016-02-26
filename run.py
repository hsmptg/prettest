import os
from app import create_app, socketio
from flask.ext.script import Manager
# import time
# from threading import Thread
#
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


# @socketio.on('connect', namespace='/rfid')
# def test_connect():
#     print("Conected!!!")
#     socketio.emit('cnt', {'value': 33}, namespace='/rfid')
#
#
# @socketio.on('my event', namespace='/rfid')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))


# counter = 0
#
# def background_thread():
#     global counter, exitFlag
#
#     while not exitFlag:
#         counter += 1
#         print('counter = {}'.format(counter))
#         socketio.emit('cnt', {'value': counter}, namespace='/test')
#         time.sleep(5)
#
#     print('exit thread')


@manager.command
def run():
    # thread = Thread(target=background_thread)
    # thread.daemon = True
    # thread.start()

    # nao da para especificar o host, port da linha de comando pelo script?
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)


# @socketio.on('reset', namespace='/test')
# def reset_counter():
#     global counter
#     counter = 0


if __name__ == '__main__':
    manager.run()
