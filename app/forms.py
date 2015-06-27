from wtforms import Form, StringField, IntegerField, validators
from wtforms.validators import DataRequired


class DoctorForm(Form):                                                                                   #Not Used . Implemented by Admin ModelView
   id = IntegerField('id')
   name = StringField('Name', [validators.Length(min=4, max=25)])
   city = StringField('City', [validators.Length(min=4, max=25)])
   experience = StringField('Experience', [validators.Length(min=4, max=25)])
   number = StringField('Number', [validators.Length(10)])
   qualification = StringField('Qualification', [validators.Length(min=4, max=25)])
   fees = IntegerField('fees')
   recommendations = IntegerField('recommendations')

class SearchForm(Form):
  location = StringField('Location', validators=[DataRequired()])
  specialization = StringField('Speciality')