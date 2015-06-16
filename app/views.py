from flask import Flask, render_template, request, session, redirect, url_for
from database import init_db, db_session
from models import *
from app import app

@app.route('/', methods=['GET', 'POST'])
def home():
    doctors = Doctor.query.all()

    return render_template('index.html', doctors=doctors)


@app.route('/home')
def landingpage():
    form = SearchForm(request.form)
    return render_template('SearchForm.html',form=form)
