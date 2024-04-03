from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DECIMAL, ForeignKey,Integer, String, Text

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    username       = Column(String(32), nullable=False, unique=True)
    password_hash  = Column(String(255))
    first_name     = Column(String(32), nullable=False)
    last_name      = Column(String(32), nullable=False)
    email          = Column(String(45), nullable=False, unique = True)
    user_type      = Column(String(45), nullable=False)

    @property
    def is_active(self):
        return True
    @property
    def is_authenticated(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id

class Listing(db.Model):
    __tablename__ =  "listings"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    title       = Column(String(255), nullable=False)
    description = Column(Text)
    user_id     = Column(Integer, ForeignKey(User.id))
    image       = Column(String(255))
    price       = Column(DECIMAL(10, 2))
    
class Contact(db.Model):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name       = Column(String(45), nullable=False)
    last_name        = Column(String(45), nullable=False)
    email            = Column(String(45), nullable=False)
    message          = Column(String(255))