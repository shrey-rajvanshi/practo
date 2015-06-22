from sqlalchemy import Column, Integer, String,Text,Table,ForeignKey
from sqlalchemy.orm import relationship,backref
from database import Base
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import *
from app import app,admin
from models import *
from database import init_db, db_session
from wtforms import *
from flask_admin import Admin, form
import os.path as op
import os
from jinja2 import Markup
from flask import Flask, url_for

file_path = op.join(os.path.dirname(os.path.abspath(__file__)),'static/')

class DoctorAdmin(sqla.ModelView):
    column_display_pk = True
    #column_exclude_list = ['id']
    form_columns = ('name','email','number','experience','qualification','city','clinics','specialities','photo')
    column_searchable_list = ('name', 'id',)
    #form_excluded_columns = ('associated_doctorlist','associated_doctors')
    #inline_models = (Clinic,)
    form_extra_fields = {
        'photo': form.ImageUploadField('Image', base_path=file_path,thumbnail_size=(100, 100, True))
    }
    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',filename=form.thumbgen_filename(model.photo)))

    column_formatters = {
        'photo': _list_thumbnail
    }
    
admin.add_view(DoctorAdmin(Doctor, db_session))



class SpecialityAdmin(sqla.ModelView):
	form_excluded_columns = ('associated_specialities',)

admin.add_view(SpecialityAdmin(Speciality, db_session))




class ClinicAdmin(sqla.ModelView):
	#form_excluded_columns = ('doctors',)
	column_searchable_list = ('name', 'id')

admin.add_view(ClinicAdmin(Clinic,db_session))
