from wtforms import Form, StringField, IntegerField, validators
from wtforms.validators import DataRequired


class DoctorForm(Form):
  id = IntegerField('id')
  name = StringField('Name', validators=[DataRequired()])
  locality = StringField('Locality', validators=[DataRequired()])
  city = StringField('City', validators=[DataRequired()])
  experience = StringField('Experience', validators=[DataRequired()])
  number = StringField('Number', validators=[DataRequired()])
  qualification = StringField('Qualification', validators=[DataRequired()])
  speciality = StringField('Speciality', validators=[DataRequired()])
  fees = IntegerField('fees', validators=[DataRequired()])
  recommendations = IntegerField('recommendations', validators=[DataRequired()])


class SearchForm(Form):
 location = StringField('location', validators=[DataRequired()])
 specialization = StringField('Specialization', validators=[DataRequired()])