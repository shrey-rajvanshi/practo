from sqlalchemy import Column, Integer, String,Text,Table,ForeignKey
from sqlalchemy.orm import relationship,backref
from database import Base
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import ModelView
from app import app,admin
from models import *
from database import init_db, db_session


class DoctorAdmin(sqla.ModelView):
    column_display_pk = True
    #column_exclude_list = ['id']
    column_searchable_list = ('name', 'id')
    form_excluded_columns = ('associated_doctorlist','associated_doctors')
    inline_models = (Speciality,Clinic)


admin.add_view(DoctorAdmin(Doctor, db_session))


class SpecialityAdmin(sqla.ModelView):
	form_excluded_columns = ('associated_specialities','doctors')

admin.add_view(SpecialityAdmin(Speciality, db_session))



class ClinicAdmin(sqla.ModelView):
	form_excluded_columns = ('doctors',)



admin.add_view(ClinicAdmin(Clinic,db_session))
