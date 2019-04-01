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
    items = relationship("Item")

    @property
    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'items': [item.serialize for item in self.items]
        }

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    description = Column(String(400), nullable=False)
    title = Column(String(100), nullable=False)
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
        'id': self.id,
        'description': self.description,
        'title': self.title,
        'cat_id': self.cat_id
        }

engine = create_engine('sqlite:///categories.db')

Base.metadata.create_all(engine)
