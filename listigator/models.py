from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .database import db

class FieldEnum(db.Enum):
    juvenile = 1
    guardianships = 2
    cannabis = 3
    civil_rights = 4
    criminal = 5
    human_rights = 6
    immigration_and_naturalization = 7
    native_american_law = 8
    lgbtq = 9

# need to create a session to interact with database

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

    lists = db.relationship('List', backref='user', lazy=True)
    #below our user model, we will create our hashing functions

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
    
    def __repr__(self):
        return "<User(username='%s')>" % (
        self.username,
    )

# helper table for many to many relationship

list_lawyers = db.Table('list_lawyers',
    db.Column('lawyer_id', db.Integer, db.ForeignKey('lawyer.id'), primary_key=True),
    db.Column('list_id', db.Integer, db.ForeignKey('list.id'), primary_key=True)
)

# create a one to many relationship between users and lists 
# (each user has a collection of lists)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    
    public = db.Column(db.Boolean, nullable=False, default=False)
    
    title = db.Column(db.String(50), nullable=False)
    lawyers = db.relationship('Lawyer', secondary=list_lawyers, lazy='subquery',
        backref=db.backref('lists', lazy=True))
    
    def __init__(self, title):
        self.title = title
        
    def __repr__(self):
        return "<List(title='%s')>" % self.title

# create a many to many relationship between lists and lawyers
# (each list has a collection of lawyers)

class Lawyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    license_number =db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    
    city = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    field = db.Column(db.String(20), nullable=False)
    
    def __init__(self, city, field, license_number, name, phone, status):
        self.license_number = license_number
        self.name = name
        self.city = city
        self.phone = phone
        self.field = field
        self.status = status
    
    def __repr__(self):
        return "<Lawyer(name='%s', city='%s', status='%s', phone='%s')>" % (
        self.name,
        self.city,
        self.status,
        self.phone,
    )