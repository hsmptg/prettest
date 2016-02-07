from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
