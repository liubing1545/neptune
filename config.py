# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


# 程序配置
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEV_DATABASE_URL = \
    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    #     'postgresql://postgres:postgres@192.168.33.133:5432/Neptune'

    @staticmethod
    def init_app(app):
        pass


# 开发程序配置
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.DEV_DATABASE_URL


# 测试程序配置
class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_DATABASE_URI = Config.DEV_DATABASE_URL
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
