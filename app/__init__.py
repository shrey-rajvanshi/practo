from database import init_db, db_session
from flask import Flask
init_db()

app = Flask('app')

from app import views, models
