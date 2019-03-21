import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    description = Column(String(400), nullable=False)
    title = Column(String(100), nullable=False)
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

engine = create_engine('sqlite:///categories.db')

Base.metadata_create_all(engine)
