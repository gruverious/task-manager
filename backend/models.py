from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime , timezone,timedelta

from database import ModelBase

IST=timezone(timedelta(hours=5,minutes=30))

class User(ModelBase):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String,unique=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)

    tasks=relationship("Task",back_populates="owner")

class Task(ModelBase):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description=Column(String,nullable=True)
    completed=Column(Boolean,default=False)
    created_at=Column(DateTime,default=lambda:datetime.now(IST))

    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    owner=relationship("User",back_populates="tasks")