import os
from app import create_app
from flask.ext.script import Manager
from flask_socketio import SocketIO

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
socketio = SocketIO(app)
manager = Manager(app)

@manager.command
def run():
    socketio.run(app, host='127.0.0.1', port=5000, use_reloader=False)

if __name__ == '__main__':
    manager.run()
