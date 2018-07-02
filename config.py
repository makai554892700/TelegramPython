import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SSL_REDIRECT = False
    # 数据库相关 dialect+driver://username:password@host:port/database
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'telegram'
    PASSWORD = 'telegram'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'telegram'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
