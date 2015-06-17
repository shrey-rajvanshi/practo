from database import init_db, db_session
from flask import Flask
from flask.ext.admin import Admin
init_db()

app = Flask('app')
admin=Admin(app)
from app import views, models,admin_views,admin_models
