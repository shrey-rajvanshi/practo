from database import init_db, db_session
from flask import Flask
from flask.ext.admin import Admin
init_db()

app = Flask('app')

app.config['UPLOAD_FOLDER'] = "/static/images/"
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
admin=Admin(app)
from app import views, models,admin_views,admin_models
