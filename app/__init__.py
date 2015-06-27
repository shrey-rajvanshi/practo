from database import init_db, db_session
from flask import Flask
from flask.ext.admin import Admin
from flask.ext.security import current_user, login_required
from flask.ext.security import  RoleMixin, Security,  SQLAlchemyUserDatastore
from models import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

init_db()

app = Flask('app')

app.config['UPLOAD_FOLDER'] = "/static/"
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024						#2 Mb limit for uploads

from app import views, models,admin_views,admin_models



'''
@login_manager.user_loader
def load_user(userid):
	u=User.get(userid)
	if u :
		return u
	else :
		return None


		'''