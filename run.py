import os
import time
from app import create_app
from flask.ext.script import Manager
from flask_socketio import SocketIO
from threading import Thread
import eventlet
eventlet.monkey_patch()


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
socketio = SocketIO(app, async_mode='eventlet')
manager = Manager(app)
counter = 0


def background_thread():
    global counter

    while True:
        print('counter = {}'.format(counter))
        counter += 1
        socketio.emit('cnt', {'value': counter}, namespace='/test')
        time.sleep(5)


@manager.command
def run():
    thread = Thread(target=background_thread)
    thread.daemon = True
    thread.start()

    # nao da para especificar o host, port da linha de comando pelo script?
    socketio.run(app, host='127.0.0.1', port=5000, use_reloader=False)


@socketio.on('reset', namespace='/test')
def reset_counter():
    global counter
    counter = 0


if __name__ == '__main__':
    manager.run()
