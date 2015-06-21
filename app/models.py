from sqlalchemy import Column, Integer, String,Text,Table,ForeignKey
from sqlalchemy.orm import relationship,backref
from database import Base
from werkzeug import secure_filename

class Doctor(Base):                                           #Doctor details
   __tablename__ = 'doctor_details'
   id = Column(Integer,primary_key = True)
   name = Column(String(64))
   email = Column(String(100))
   experience = Column(Integer)                               #experience in years
   number = Column(String(10))
   fees = Column(Integer)                                     #should be a relationship attribute of the relationship(doctor-clinic).as of now.
   recommendations = Column(Integer)                          #no Of recommendations
   qualification = Column(Text)                               #stored as text. Maybe split into name, institution etc.
   city=Column(String(20))                                    #main location of a doctor. 
   status = Column(String(200))
   specialities = relationship("Speciality",secondary="assoc_doc_spec_table")
   clinics = relationship("Clinic",secondary="assoc_doc_clinic_table")
   photo = Column(String(100))


   def __init__(self, name=None, locality=None,city=None,
       experience=None,number=None,qualification=None,
       speciality=None, fees=None, recommendations=None):
       self.name = name
       self.locality = locality
       self.city = city
       self.experience = experience
       self.number = number
       self.qualification = qualification
       self.speciality = speciality
       self.fees = fees
       self.recommendations = recommendations

   def __repr__(self):
        return 'Dr. %r' % (self.name)


class Speciality(Base):
    __tablename__ = 'Speciality_details'
    id = Column(Integer,primary_key = True)
    name = Column(String(40),unique=True)
    doctors = relationship(
        "Doctor",
        secondary='assoc_doc_spec_table')

    def __init__(self,name=""):
        self.name = name

    def __repr__(self):
        return str(self.name)



class doc_spec(Base):                                       #Association object - for implementing ManytoMany relationship
    __tablename__ = 'assoc_doc_spec_table'
    doc_id = Column(Integer, ForeignKey('doctor_details.id'), primary_key=True)
    spec_id = Column(Integer, ForeignKey('Speciality_details.id'), primary_key=True)
    #rel_speciality = relationship(Speciality, backref=backref("associated_specialities",cascade="save-update, merge,delete, all,delete-orphan"))
    #rel_doctor = relationship(Doctor, backref=backref("associated_doctors",cascade="save-update, merge,delete, all,delete-orphan"))

    def __repr__(self):
        return 'Doc Spec b/w :' + str(self.doc_id)+" and "+str(self.spec_id)

class Clinic(Base):
  __tablename__ ="clinic_details"
  id = Column(Integer,primary_key = True)
  name = Column(String(100))
  city= Column(String(20))  
  locality = Column(String(400))
  address = Column(Text)
  about = Column(Text)
  timings = Column(String(500))
  services = Column(Text)
  lattitude = Column(String(500))              # check later
  longitude = Column(String(500))              #check later
  doctors = relationship("Doctor",secondary='assoc_doc_clinic_table')

  def __repr__(self):
        return str(self.name)


class assoc_doc_clinic(Base):
  __tablename__ ="assoc_doc_clinic_table"
  doc_id = Column(Integer, ForeignKey('doctor_details.id'), primary_key=True)
  clinic_id = Column(Integer, ForeignKey('clinic_details.id'), primary_key=True)
  #rel_doctor = relationship(Doctor, backref=backref("associated_doctorlist",cascade="save-update, merge,delete, all,delete-orphan"))
  #rel_clinic = relationship(Clinic,backref=backref("associated_clinics",cascade="save-update, merge,delete, all,delete-orphan"))
  fees = Column(Integer)
  timings= Column(String(300))


  def __repr__(self):
        return 'Doc Spec b/w :' + str(self.doc_id)+" and "+str(self.clinic_id)


