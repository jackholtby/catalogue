from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

newCategory = Category(name = "Cricket")
session.add(newCategory)
session.commit()

newItem = Item(title = "Wickets", description = "The latest and greatest wickets for your cricket set.", cat_id = "1")
session.add(newItem)
session.commit()

newItem = Item(title = "Ball", description = "Cricket ball signed by Brett Lee.", cat_id = "1")
session.add(newItem)
session.commit()

newItem = Item(title = "Bat", description = "Because I'm ...the Batsman", cat_id = "1")
session.add(newItem)
session.commit()

newItem = Item(title = "Wicket Keeper Glove", description = "For catching all those 'Howisat!' shots...", cat_id = "1")
session.add(newItem)
session.commit()

newCategory = Category(name = "Ultimate Frisbee")
session.add(newCategory)
session.commit()

newItem = Item(title = "", description = "", cat_id = "2")
session.add(newItem)
session.commit()

newItem = Item(title = "", description = "", cat_id = "2")
session.add(newItem)
session.commit()

newItem = Item(title = "", description = "", cat_id = "2")
session.add(newItem)
session.commit()

newItem = Item(title = "", description = "", cat_id = "2")
session.add(newItem)
session.commit()

newCategory = Category(name = "Rugby")
session.add(newCategory)
session.commit()

newCategory = Category(name = "Grass Hockey")
session.add(newCategory)
session.commit()

newCategory = Category(name = "Running")
session.add(newCategory)
session.commit()

newCategory = Category(name = "Swimming")
session.add(newCategory)
session.commit()
