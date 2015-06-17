from sqlalchemy import Column, Integer, String,Text,Table,ForeignKey
from sqlalchemy.orm import relationship,backref
from database import Base

class Doctor(Base):                                           #Doctor details
   __tablename__ = 'doctor_details'
   id = Column(Integer,primary_key = True)
   name = Column(String(64))
   experience = Column(Integer)
   number = Column(Integer)
   fees = Column(Integer)
   recommendations = Column(Integer)
   qualification = Column(Text)
   city=Column(String(20))
   specialities = relationship("Speciality",secondary="association")


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
        secondary='association')

    def __init__(self):
        self.name = ""

    def __repr__(self):
        return self.name



class doc_spec(Base):                                       #Association object
    __tablename__ = 'association'
    doc_id = Column(Integer, ForeignKey('doctor_details.id'), primary_key=True)
    spec_id = Column(Integer, ForeignKey('Speciality_details.id'), primary_key=True)
    rel_speciality = relationship(Speciality, backref=backref("associated_speciality",cascade="save-update, merge,delete, all,delete-orphan"))
    rel_doctor = relationship(Doctor, backref=backref("associated_doctor",cascade="save-update, merge,delete, all,delete-orphan"))

    def __repr__(self):
        return 'Relationship b/w :' + str(self.doc_id)+" and "+str(self.spec_id)

