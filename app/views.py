from flask import Flask, render_template, request, session, redirect, url_for
from database import init_db, db_session
from models import *
from app import app
from forms import *

@app.route('/home', methods=['GET', 'POST'])
def home():                                                             #display all doctors . No specific use.
    doctors = Doctor.query.all()
    specs = Speciality.query.all()
    isblank=False
    if(len(doctors)==0):
        isblank=True
    return render_template('index.html', doctors=doctors,blank_flag=isblank)

@app.route('/search/<location>')
@app.route('/search/<location>/')                                        #Trailing slash issue solved
def searchbylocation(location):                                          #Search doctors by city.
    doctors = Doctor.query.filter(Doctor.city==location)
    isblank=False
    if(doctors.count()==0):
        isblank=True
    return render_template('index.html', doctors=doctors,blank_flag=isblank)

@app.route('/search/<location>/<speciality>/', methods=['GET', 'POST'])
@app.route('/search/<location>/<speciality>', methods=['GET', 'POST'])                  
def searchbyspecialitynlocation(location,speciality):                                       #main search function by city and speciality
    searchedSpecId=Speciality.query.filter(Speciality.name==speciality)[0].id                 #Id of searched speciality
    listOfDoc_specs = doc_spec.query.filter(doc_spec.spec_id==searchedSpecId)                 #list of all associated doc_spec(associated object) IDs
    doctors=[]                                                                                
    isblank=False
    for doc_spec_object in listOfDoc_specs:                                                 #get doctors in list of associated objects' ids
        doc_id=doc_spec_object.doc_id
        if(Doctor.query.get(int(doc_id)).city ==location):                                  #filter selected Doctor objects on location
            doctors.append(Doctor.query.get(int(doc_id)))

    if(doctors.count()==0):
        isblank=True
    return render_template('index.html', doctors=doctors,blank_flag=isblank)

@app.route('/')
def landingpage():
    form = SearchForm(request.form)
    return render_template('SearchForm.html',form=form)
