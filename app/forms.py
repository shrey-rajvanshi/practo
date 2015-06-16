from wtforms import Form, StringField, IntegerField, validators

class DoctorForm(Form):
   id = IntegerField('id')
   name = StringField('Name', [validators.Length(min=4, max=25)])
   locality = StringField('Locality', [validators.Length(min=4, max=25)])
   city = StringField('City', [validators.Length(min=4, max=25)])
   experience = StringField('Experience', [validators.Length(min=4, max=25)])
   number = StringField('Number', [validators.Length(10)])
   qualification = StringField('Qualification', [validators.Length(min=4, max=25)])
   speciality = StringField('Speciality', [validators.Length(min=4, max=25)])
   fees = IntegerField('fees')
   recommendations = IntegerField('recommendations')


class SearchForm(Form):
  location = StringField('location', [validators.Length(min=4, max=25)])
  specialization = StringField('Specialization', [validators.Length(min=4, max=25)])