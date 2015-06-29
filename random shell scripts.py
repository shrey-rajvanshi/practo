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





for i in range(10,60):
     i=str(i)
     name = "Name:"+i
     email = "Email"+i+"@practo.com"
     experience = 10+int(i)
     number = '09999912'+i
     city = "Bangalore"
     salutation = "Dr."
     d= Doctor(name=name,email=email,experience=experience,number=number,city=city,salutation = salutation)
     db_session.add(d)


-------------------------------------------------------------------------------------------------------------------------------------



#create country first. default. Set default city (country_id ) to that.
# override locality form, or add city baCKREF

from app import app
from app.database import *
from app.models import *


#Creating users
u1 = User(name= "Admin",email = "admin@practo.com",password = "pass",active = 1)
u2 = User(name = "Data Entry Team",email = "dataentry@practo.com",password = "pass")
r1= Role(name="admin" , description = "Admin rights")
r2 = Role(name = "DataEntry",description = "Data Entry rights")
u3= User(name = "Shrey", email = "shrey@practo.com",password = "pass")
db_session.add(u1)
db_session.add(u2)
db_session.add(u3)
db_session.add(r1)
db_session.add(r2)

u1.roles.append(r1)
u2.roles.append(r2)

c = Country(name = "India")
db_session.add(c)

l = Locality(name = "J P Nagar")
db_session.add(l)

db_session.commit()





#------------------------------------------------------------------------------------------------------------------------------------


#add to elastic search(():
 #    speciality, name, locality.name,


from app import app
from app.database import *
from app.models import *

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

for d in Doctor.query.all():
     print "querying : ",d.name
     doc = {'name':d.name, "id":d.id,"city":City.query.get(d.city).name}
     es.index(index="practo_index", doc_type='doctors',body=doc)
     
for clinic in Clinic.query.all():
    doc = {"id":clinic.id,"name":clinic.name,"city":City.query.get(clinic.city).name} 
    es.index(index="practo_index", doc_type='clinics',body=doc)
     

for spec in Speciality.query.all():
    doc = {"name":spec.name}
    es.index(index="practo_index", doc_type='specialities',body=doc)
     
for l in Locality.query.all():
    localityname = l.name
    cityname = City.query.get(l.city_id).name
    doc = {"name":localityname,"city":cityname,"type":"locality"}
    es.index(index="practo_index", doc_type='location',body=doc)
