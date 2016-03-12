import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:regmed@127.0.0.1/test1'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # Para evitar o aviso:
    # UserWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead
    # and will be disabled by default in the future.
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
