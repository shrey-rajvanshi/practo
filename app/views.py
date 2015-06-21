from flask import Flask, render_template, request, session, redirect, url_for
from database import init_db, db_session
from models import *
from app import app
from forms import *
from werkzeug import secure_filename


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
    clinic= Clinic.query.filter(Clinic.city==location).first()
    isblank=False
    if(doctors.count()==0):
        isblank=True
    return render_template('index.html', doctors=doctors,blank_flag=isblank,clinic=clinic)

@app.route('/search/<location>/<speciality>/', methods=['GET', 'POST'])
@app.route('/search/<location>/<speciality>', methods=['GET', 'POST'])                  
def searchbyspecialitynlocation(location,speciality):                                       #main search function by city and speciality
    searchedSpecId=Speciality.query.filter(Speciality.name==speciality)[0].id               #Id of searched speciality
    listOfDoc_specs = doc_spec.query.filter(doc_spec.spec_id==searchedSpecId)               #list of all associated doc_spec(associated object) IDs
    doctors=[]                                                                                
    isblank=False
    clinic = Clinic.query.filter(Clinic.city==location).first()                             #To-Do: add clinic speciality
    for doc_spec_object in listOfDoc_specs:                                                 #get doctors in list of associated objects' ids
        doc_id=doc_spec_object.doc_id
        if(Doctor.query.get(int(doc_id)).city ==location):                                  #filter selected Doctor objects on location
            doctors.append(Doctor.query.get(int(doc_id)))

    if(doctors.count()==0):
        isblank=True
    return render_template('index.html', doctors=doctors,blank_flag=isblank,clinic = clinic)

@app.route('/')
def landingpage():
    form = SearchForm(request.form)
    return render_template('SearchForm.html',form=form)






ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''  <!doctype html>    <title>Upload new File</title>    <h1>Upload new File</h1>    <form action="" method=post enctype=multipart/form-data>      <p><input type=file name=file>         <input type=submit value=Upload>   </form>    '''



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



