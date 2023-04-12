from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, enum

class FieldEnum(enum.Enum):
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)

    username = Column(String(50))
    password_hash = Column(String(128))

    #below our user model, we will create our hashing functions

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return "<User(name='%s', username='%s')>" % (
        self.name,
        self.username,
    )

# create a one to many relationship between users and lists 
# (each user has a collection of lists)

class List(Base):
    __tablename__ = "lists"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    title = Column(String(50), nullable=False)
    
    user = relationship("User", back_populates="lists")

    def __repr__(self):
        return "<List(title='%s')>" % self.title

User.lists = relationship("List", order_by=List.id, back_populates="user")

# create a many to many relationship between lists and lawyers
# (each list has a collection of lawyers)

class Lawyer(Base):
    __tablename__ = "lawyers"
    
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("lists.id"))
    
    license_number = Column(Integer(20), nullable=False)
    name = Column(String(50), nullable=False)
    
    city = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)
    
    field = Column(String(20), nullable=False)
    
    user = relationship("List", back_populates="lawyers")
    
    def __repr__(self):
        return "<Lawyer(name='%s', city='%s', status='%s', phone='%s')>" % (
        self.name,
        self.city,
        self.status,
        self.phone,
    )

List.lawyers = relationship("Lawyer", order_by=Lawyer.id, back_populates="lists")