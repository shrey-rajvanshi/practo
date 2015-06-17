from app import app
ctx = app.test_request_context()
ctx.push()
from app.models import *
from app.views import *

User.query.all()
[<User u'Shrey'>, <User u'Aradhya'>, <User u'Dhruv'>, <User u'saurabh'>, <User u'Shreytestingid'>, <User u'Dhruv testing id'>]
Speciality.query.all()
[]


d= Doctor("Dr.Shrey")
db_session.add(d)

from app.views import *
spec = Speciality(id=1,name= "Dentist")
db_session.add(spec)
db_session.commit()
Speciality.query.all()

for i in ["Pediatrician","Gynecologist","General Physician"]:
	spec = Speciality(name = i)
	db_session.add(spec)

db_session.commit()



d=Doctor.query.get(3)
s=Speciality.query.get(1)
link = doc_spec(left_id = 3,right_id=1,extra_data="Random data")

print Doctor.query.get(int(doc_spec.query.filter(doc_spec.left_id==3)[0].right_id))



a= Doctor("Dr. Aardhya",locality="jp nagar",city="Mumbai",experience=13,number=9080080800,qualification="MD,MBBS AEGT",fees=120, recommendations=12)
db_session.add(a)
db_session.commit()


link1 = doc_spec(doc_id = 5,spec_id=1,extra_data="Random data")
db_session.add(link1)
db_session.commit()
