import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #设置安全密匙
    SECRET_KEY = 'maybe you want to die'
    #设置图片保存地址
    UPLOADED_PHOTOS_DEST = os.getcwd() + '/static/asset/helmet/'
    #UPLOADED_AVATAR_DEST = os.getcwd() + '/static/asset/avatars/'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #Flask Mail Config
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True 
    MAIL_USE_TSL = False
    MAIL_USERNAME = '2963864804@qq.com'
    MAIL_PASSWORD = 'uphsbeyhrmeoddac'
    MAIL_SUPPRESS_SEND = False
    ADMINS = ['2963864804@qq.com']