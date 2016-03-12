from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, async_mode='eventlet')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .production import production as production_blueprint
    app.register_blueprint(production_blueprint)

    return app
