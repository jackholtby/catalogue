import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    """
    Registered User information is stored in this table
    """

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(400), nullable=False)
    picture = Column(String(250))

    # JSON format for the data.
    @property
    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'picture': self.picture
    }

class Category(Base):
    """
    Category information is stored here.
    """

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship("Item")


    # JSON format for the data.
    @property
    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        # Loop through all items found within category.
        'items': [item.serialize for item in self.items]
        }

class Item(Base):
    """
    Pre-generated and newly added items are stored in this table.
    """

    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    description = Column(String(400), nullable=False)
    title = Column(String(100), nullable=False)
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # JSON format for the data.
    @property
    def serialize(self):
        return {
        'id': self.id,
        'description': self.description,
        'title': self.title,
        'cat_id': self.cat_id,
        'user_id': self.user_id
        }

engine = create_engine('sqlite:///categories.db')

Base.metadata.create_all(engine)
