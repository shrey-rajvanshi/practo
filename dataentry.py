from app import app
ctx = app.test_request_context()
ctx.push()
from app.models import *
from app.views import *
from app.database import *


for i in ["Cosmetologist","Gynecologist","General Physician","Dentist","Dermatologist","Pediatrician"]:
	spec = Speciality(name = i)
	db_session.add(spec)

db_session.commit()


for i in range(10,60):
     i=str(i)
     name = "Name:"+i
     email = "Email"+i+"@practo.com"
     experience = 10+int(i)%20
     number = '09999912'+i
     location = int(i)%5+1
     salutation = "Dr."
     d= Doctor(name=name, email = email, experience=experience, locality = location, number = number, qualification = "MBBS , MD", recommendations = 73%int(i), salutation = salutation, verified=1, published=1)
     db_session.add(d)


for i in range(10,20):
	name = "Clinic"+str(i)
	locality = i%5+1
	address = "Address of Clinic"+str(i)
	about = "The about field of Clinic"+str(i)
	clinic = Clinic(name=name, locality = locality, address=address )
	db_session.add(clinic)

db_session.commit()

for d in Doctor.query.all():
	b = assoc_doc_clinic(doc_id = d.id, clinic_id = d.id%5+5)
		db_session.add(b)




#add to elastic search(():
 #    speciality, name, locality.name,


from run import app
from database import *
from models import *

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

for d in Doctor.query.all():
     print "querying : ",d.name
     doc = {'name':d.name, "id":d.id,"city":City.query.get(Locality.query.get(d.locality).city_id).name}
     es.index(index="practo_index", doc_type='doctors',body=doc)
     
for clinic in Clinic.query.all():
    doc = {"id":clinic.id,"name":clinic.name,"city":City.query.get(Locality.query.get(clinic.locality).city_id).name} 
    es.index(index="practo_index", doc_type='clinics',body=doc)
     

for spec in Speciality.query.all():
    doc = {"name":spec.name}
    es.index(index="practo_index", doc_type='specialities',body=doc)
     
for l in Locality.query.all():
    localityname = l.name
    cityname = City.query.get(l.city_id).name
    doc = {"name":localityname,"city":cityname,"type":"locality"}
    es.index(index="practo_index", doc_type='location',body=doc)



