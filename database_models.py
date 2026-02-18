from database import Base
from sqlalchemy import Column, Integer, String, Float,Boolean

class Product(Base):
    __tablename__="Products"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    price= Column(Float)
    quantity = Column(Integer)

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    email=Column(String,unique=True,index=True)
    hashed_pw=Column(String)
    role=Column(String,default="user")
    is_active = Column(Boolean, default=True) 

