from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

class Newsletter(Base):
    __tablename__ = "newsletters"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
