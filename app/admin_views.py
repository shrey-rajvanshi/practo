from flask import Flask, Response,make_response
from flask.ext.admin import Admin, BaseView, expose
from database import init_db, db_session
from models import *
from app import app
from forms import *
from flask.ext.security import current_user, login_required


@app.route('/generate')
def generate_large_csv():
    def generate():
        r = requests.get('http://httpbin.org/stream/20', stream=True)
        for row in r.iter_lines():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')



@app.route('/download')
def downloadall():
	csv = ""
	csv+=("Name"+","+"Email"+","+"Number"+","+"City"+","+"status"+","+"qualification"+"\n")
	for d in Doctor.query.all():
		csv+=(str(d.name)+","+str(d.email)+","+str(d.number)+","+str(d.city)+","+str(d.status)+","+str(d.qualification)+"," +"\n")
	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=AllDoctors.csv"
	return response



@app.route('/downloadpublished')
def downloadallpublished():
	csv = ""
	csv+=("Name"+","+"Email"+","+"Number"+","+"City"+","+"status"+","+"qualification"+"\n")
	for d in Doctor.query.filter(Doctor.published==1):
		csv+=(str(d.name)+","+str(d.email)+","+str(d.number)+","+str(d.city)+","+str(d.status)+","+str(d.qualification)+"," +"\n")
	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=AllPublishedDoctors.csv"
	return response