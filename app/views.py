from flask import Flask, render_template, request, session, redirect, url_for,g,jsonify
from database import init_db, db_session
from models import *
from app import app
from forms import *
from werkzeug import secure_filename
from flask.ext.security import current_user, login_required, SQLAlchemyUserDatastore
from flask_security.datastore import UserDatastore
from flask.ext.login import login_user, logout_user, current_user, login_required,LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import roles_required
import json



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
    doctors={}
    doctors['result'] = Doctor.query.filter(Doctor.city==location)
    clinic= Clinic.query.filter(Clinic.city==location).first()
    isblank=False
    if(len(doctors)==0):
        isblank=True
    return render_template('index.html',page=1, doctors=doctors,blank_flag=isblank,clinic=clinic)

  
@app.route('/search/<location>/<speciality>/', methods=['GET', 'POST'])
@app.route('/search/<location>/<speciality>', methods=['GET', 'POST'])                  
@app.route('/search/<location>/<speciality>/<int:page>', methods=['GET', 'POST'])                  
def searchbyspecialitynlocation(location,speciality,page=1):                                       #main search function by city and speciality
   pagesize = 5
   try:
    searchedSpecId=Speciality.query.filter(Speciality.name == speciality).first().id                 #Id of searched speciality
   except:
    return "Speciality Not found. <a href = './../../'>Go back</a>"

   listOfDoc_specs = doc_spec.query.filter(
     doc_spec.spec_id == searchedSpecId).offset(
       int((page-1)*pagesize)).limit(int(pagesize + 1)).all()                              #list of all associated doc_spec(associated object) IDs
   print listOfDoc_specs
   doctors = {}
   doctors['result'] = []
   clinic = Clinic.query.filter(Clinic.city==location).first()                             #To-Do: add clinic speciality

   for doc_spec_object in listOfDoc_specs:                                                 #get doctors in list of associated objects' ids
       doc_id = doc_spec_object.doc_id
       if(Doctor.query.get(int(doc_id)).city.lower() == location.lower() ):                #and Doctor.query.get(int(doc_id)).published==1):                                  #filter selected Doctor objects on location
           doctors['result'].append(Doctor.query.get(int(doc_id)))
   
   print type(doctors['result'])

   if len(doctors['result']) > pagesize:
       doctors['hasMore'] = True
       doctors['result'].pop()
       doctors['nextLink'] = str(page + 1)
   else:
       doctors['hasMore'] = False
   if page > 1:
       doctors['prevLink'] = str(page - 1)
   
   isblank=False
   if(len(doctors['result']) == 0):
       isblank=True
   return render_template('index.html',pages=page, doctors=doctors,blank_flag=isblank,clinic = clinic,  location=location,speciality=speciality)

@app.route('/')
def landingpage():
    form = SearchForm(request.form)
    city = ['Bangalore','Mumbai','Delhi']
    return render_template('SearchForm.html',form=form,cities=city)



@app.route('/profile/<doc_id>')
def doctor_profile(doc_id):
    d=Doctor.query.get(doc_id)
    clinics = d.clinics
    return render_template('profilePage.html',doctor = d, clinics =clinics)



@app.route('/getprofile/<doc_id>')
def get_doctor_profile(doc_id):
    d=Doctor.query.get(doc_id)
    doctor = {}
    for k,v in d.__dict__.iteritems():
      if(k[0]!='_'):
        doctor[k]=v
    response= {'data': d.serialize(), 'success':True}
    return json.dumps(response)
    #return json.dumps(d.__dict__)

@app.route('/getallprofile')
def get_all_doctors():
  return json.dumps(Doctor.query.all())






#----------------------------------------------------------Authentication stuff------------------------------------------------------#



db = SQLAlchemy(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/logincheck/')
@login_required
def logina():
    return 'Proved: You are logged in .'

@app.route('/loginadmin')
@roles_required('admin')
def loginb():
    return 'Test:You need to login to be able to make changes'


@app.route('/login/check', methods=['post'])
def login_check():
    # validate username and password
    user = User.query.filter(User.email==request.form['email']).first()
    if (user and user.password == request.form['password']):
        login_user(user)
        flash('Logged in successfully.')
    
    else:
        return ('Username or password incorrect')
    return "Redirect to admin link here"
