# -*- coding: utf-8 -*-
from config import Config
from flask import Flask
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_mail import Mail
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'You must login to acess this page'
login.login_message_category = 'info'


photos = UploadSet('photos', IMAGES) #创建一个set
configure_uploads(app, photos) #注册并完成相应配置
patch_request_class(app)  # 限制文件大小 set maximum file size, default is 16MB

avatars = UploadSet('photos', IMAGES) #创建一个set
configure_uploads(app, avatars) #注册并完成相应配置
patch_request_class(app)  # 限制文件大小 set maximum file size, default is 16MB


from app.routes import *
from app.models import *
from app.errors import *
