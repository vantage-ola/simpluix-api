import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://ola:rkEVq9Z9gZXIsRem@192.168.64.2/simpluix-v1'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')