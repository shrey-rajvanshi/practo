from sqlalchemy import Column,  Integer,  String, Text, Table, ForeignKey,\
  DateTime,  Boolean
from sqlalchemy.orm import relationship, backref
from database import Base
from werkzeug import secure_filename
from flask.ext.security import  RoleMixin,  Security, \
   SQLAlchemyUserDatastore, UserMixin,  utils

class Doctor(Base):                                                                   
  __tablename__ = 'doctor_details'
  id = Column(Integer, primary_key = True)
  name = Column(String(64))
  email = Column(String(100))
  experience = Column(Integer)                                                        
  number = Column(String(10))
  recommendations = Column(Integer)                                                   
  qualification = Column(Text)                                                        
  locality = Column(Integer, ForeignKey('localities.id'))                                   
  status = Column(String(200))
  specialities = relationship("Speciality",  secondary="assoc_doc_spec_table")
  clinics = relationship("Clinic",  secondary="assoc_doc_clinic_table")
  photo = Column(String(100))
  salutation = Column(String(10))                                                                   #Salutation : Mr, Dr,  etc.
  verified = Column(Integer)                                                                        #Whether doctor profile has been verified.
  published = Column(Integer)                                                                       #Whether doctor profile is live.


  def __init__(self,  name = None, locality = None,email = None, 
      experience = None,number = None, qualification = None,  
      recommendations = None, salutation = None):
      self.name = name
      self.email = email
      self.experience = experience
      self.locality = locality
      self.number = number
      self.qualification = qualification
      self.recommendations = recommendations
      self.status = 0
      self.salutation = salutation
      self.verified = 0
      self.published = 0

  def __repr__(self):
        return str(self.salutation) + str(self.name)

  def serialize(self):
    return {
    'id':self.id,
    'name':self.name,
    'email':self.email,
    'experience':self.experience,
    'recommendations':self.recommendations,
    'city':City.query.get(Locality.query.get(self.locality).city_id).name,
    'specialities':[str(speciality) for speciality in self.specialities],
    'clinics':[str(clinic) for clinic in self.clinics]
    }

class Country(Base):
  __tablename__ = 'countries'
  id = Column(Integer, primary_key = True)
  name = Column(String(60))


class City(Base):
  __tablename__ = 'cities'
  id = Column(Integer, primary_key = True)
  name = Column(String(60))
  country_id = Column(Integer, ForeignKey('countries.id'))

  def __init__(self, name = None):
    self.name = name
    self.country_id = 1


class Locality(Base):
  '''To-do : add support for multiple : Bengaluru and Bangalore, 
      Mumbai and Bombay should point to same id.      '''
  __tablename__ = 'localities'
  id = Column(Integer, primary_key = True)
  name = Column(String(60))
  city_id = Column(Integer, ForeignKey('cities.id'))        




class Speciality(Base):
    __tablename__ = 'Speciality_details'
    id = Column(Integer, primary_key = True)
    name = Column(String(40), unique=True)
    doctors = relationship(
        "Doctor", 
        secondary ='assoc_doc_spec_table')

    def __init__(self, name = ""):
        self.name = name

    def __repr__(self):
        return str(self.name)



class doc_spec(Base):                                       
    __tablename__ = 'assoc_doc_spec_table'
    doc_id = Column( Integer,  ForeignKey('doctor_details.id'), 
      primary_key=True)
    spec_id = Column( Integer,  ForeignKey('Speciality_details.id'),
     primary_key=True)
    def __repr__(self):
        return 'Doc Spec  b/w :' + str(self.doc_id)+" and "+str(self.spec_id)

class Clinic(Base):
  __tablename__ ="clinic_details"
  id = Column(Integer, primary_key = True)
  name = Column(String(100))
  locality = Column(Integer,ForeignKey('localities.id'))
  address = Column(Text)
  about = Column(Text)
  timings = Column(String(50))
  services = Column(Text)
  lattitude = Column(String(50))              # check later
  longitude = Column(String(50))              #check later
  doctors = relationship("Doctor", secondary='assoc_doc_clinic_table')

  def __repr__(self):
        return str(self.name)

  def __init__(self, name="", locality=1, address=''):
    self.name = name
    self.address=address
    self.locality = locality

class assoc_doc_clinic(Base):
  __tablename__ = "assoc_doc_clinic_table"
  doc_id = Column(Integer,  ForeignKey('doctor_details.id'), primary_key=True)
  clinic_id = Column(Integer, ForeignKey('clinic_details.id'), primary_key=True)
  fees = Column(Integer)
  timings = Column(String(300))


  def __repr__(self):
        return 'Doc Spec:' + str(self.doc_id) + " and " + str(self.clinic_id)


# Create a table to support a many-to-many relationship between Users and Roles
roles_users = Table(
    'roles_users', 
    Base.metadata, 
    Column('user_id',  Integer,  ForeignKey('users.id'),  primary_key=True), 
    Column('role_id',  Integer,  ForeignKey('roles.id'),  primary_key=True)
)


# Role class
class Role(Base,  RoleMixin):
  __tablename__ = "roles"
  # Our Role has three fields,  ID,  name and description
  id = Column(Integer(),  primary_key=True)
  name = Column(String(80),  unique=True)
  description = Column(String(255))
  def __str__(self):
      return self.name

  def __hash__(self):
      return hash(self.name)





# User class
class User(Base,  UserMixin):
    __tablename__ = "users"
    id = Column(Integer,  primary_key=True)
    name = Column(String(30))
    email = Column(String(255),  unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship(
        'Role', 
        secondary = roles_users, 
        backref = backref('users',  lazy = 'dynamic')
    )