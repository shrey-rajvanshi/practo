from sqlalchemy import Column, Integer, String,Text,Table,ForeignKey
from sqlalchemy.orm import relationship,backref
from database import Base
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import *
from app import app
from views import *
from models import *
from database import init_db, db_session
from wtforms import *
from flask_admin import Admin, form,AdminIndexView
import os.path as op
import os
from jinja2 import Markup
from flask import Flask, url_for,redirect,request
from flask.ext.security import current_user, login_required, RoleMixin, Security,  SQLAlchemyUserDatastore, UserMixin, utils,current_user
from flask.ext.login import current_user




file_path = op.join(os.path.dirname(os.path.abspath(__file__)),'static/')


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        arg1 = 'Hello'
        return self.render('admin/index.html', arg1=arg1)

    def is_accessible(self):
        if not current_user.is_active() or not current_user.is_authenticated():
            return False

        if current_user.has_role('admin'):
            return True

        return False

admin = Admin(app, index_view=MyHomeView())



class DoctorAdmin(sqla.ModelView):
    column_display_pk = True
    column_exclude_list = ['id','fees','recommendations','published']
    form_columns = ('salutation','name','email','number','experience','qualification',
        'city','clinics','specialities','photo','verified')
    column_searchable_list = ('name', 'id',)
    column_editable_list = ('name','email','experience','qualification','city','verified')
    column_filters = ('city', 'email','name')
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
    '''
    def __init__(self):
        print "called"
    
    def after_model_change(self, form, model, is_created):

        return super(UserAdmin, self).after_model_change(form, model, is_created)
    '''    

admin.add_view(DoctorAdmin(Doctor, db_session))



class SpecialityAdmin(sqla.ModelView):
	form_excluded_columns = ('associated_specialities',)

admin.add_view(SpecialityAdmin(Speciality, db_session))


class ClinicAdmin(sqla.ModelView):
    form_columns = ('doctors',"name","city","locality",'address')
    column_searchable_list = ('name', 'id')
    column_exclude_list = ['id','about','timings','lattitude','longitude']

admin.add_view(ClinicAdmin(Clinic,db_session))

class LocalityAdmin(sqla.ModelView):
    #form_excluded_columns = ('associated_specialities',)
    column_searchable_list = ('name',)


admin.add_view(LocalityAdmin(Locality, db_session))

admin.add_view(ModelView(City,db_session))

admin.add_view(ModelView(Country,db_session))