from flask import Flask, render_template, request, session, redirect, url_for
from database import init_db, db_session
from models import *
from app import app

@app.route('/', methods=['GET', 'POST'])
def home():
    doctors = Doctor.query.all()
    specs = Speciality.query.all()
    return render_template('index.html', doctors=doctors)

@app.route('/search/<location>')
def searchbylocation(location):
    doctors = Doctor.query.filter(Doctor.city==location)
    return render_template('index.html', doctors=doctors)


@app.route('/searchspec/<speciality>', methods=['GET', 'POST'])
def searchbyspeciality(speciality):
    listOfDocIds = doc_spec.query.filter(doc_spec.doc_id==1)
    users=[]
    for i in listOfDocIds:
        doctors.append(Doctor.query.get(int(i.spec_id)))
    return render_template('index.html', doctors=doctors)

@app.route('/search/<location>/<speciality>', methods=['GET', 'POST'])
def searchbyspecialitynlocation(location,speciality):
    searchedSpecId=Speciality.query.filter(Speciality.name==speciality)[0].id
    listOfDoc_specs = doc_spec.query.filter(doc_spec.spec_id==searchedSpecId)
    doctors=[]
    stra=""
    for doc_spec_object in listOfDoc_specs:
        stra+=str(doc_spec_object)
        doc_id=doc_spec_object.doc_id
        if(Doctor.query.get(int(doc_id)).city ==location):
            doctors.append(Doctor.query.get(int(doc_id)))
    return render_template('index.html', doctors=doctors)

@app.route('/home')
def landingpage():
    form = SearchForm(request.form)
    return render_template('SearchForm.html',form=form)
