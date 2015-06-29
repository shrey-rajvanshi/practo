from app import app
from app.database import *
from app.models import *

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

for d in Doctor.query.all():
     print "quering : ",d.name
     cityname = City.query.get(d.city).name
     localityname = Locality.query.get(d.locality).name
     clinics = [clinic.name for clinic in d.clinics]
     specialities = [speciality.name for speciality in d.specialities]
     doc = {'name':d.name, 'city':cityname, 'locality':localityname, "id":d.id, 'specialities':specialities , 'clinics' : clinics}
     es.index(index="practo_index", doc_type='doctors',body=doc)

