from sqlalchemy import Column, Integer, String,Text,Table,ForeignKey

from database import Base

class Doctor(Base):
   __tablename__ = 'doctor_details'
   id = Column(Integer,primary_key = True)
   name = Column(String(64))
   experience = Column(Integer)
   number = Column(String(500))
   fees = Column(Integer)
   recommendations = Column(Integer)
   qualification = Column(Text)
   city=Column(String(20))


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
        return '<Doctor %r>' % (self.name)

