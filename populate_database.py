from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

newCategory = Category(name="Cricket")
session.add(newCategory)
session.commit()

newUser = User(name="Caitlyn Snow", email="frosty@gmail.com")
session.add(newUser)
session.commit()

newUser = User(name="Harrison Wells", email="Harrisonwells@gmail.com")
session.add(newUser)
session.commit()

newUser = User(name="Barry Allen", email="Barryallen@gmail.com")
session.add(newUser)
session.commit()

newUser = User(name="Wally West", email="Wallywest@gmail.com")
session.add(newUser)
session.commit()

newItem = Item(
               title="Wickets",
               description="The latest and greatest\
               wickets for your cricket set.",
               cat_id="1", user_id="2")
session.add(newItem)
session.commit()

newItem = Item(title="Ball",
               description="Cricket ball signed by Brett Lee.", cat_id="1",
               user_id="1")
session.add(newItem)
session.commit()

newItem = Item(title="Bat",
               description="Because I'm ...the Batsman", cat_id="1",
               user_id="2")
session.add(newItem)
session.commit()

newItem = Item(title="Glove",
               description="For catching all those 'Howisat!' shots...",
               cat_id="1", user_id="2")
session.add(newItem)
session.commit()

newCategory = Category(name="Ultimate")
session.add(newCategory)
session.commit()

newItem = Item(title="Frisbee", description="Epic Cool frisbee",
               cat_id="2", user_id="1")
session.add(newItem)
session.commit()

newItem = Item(title="Holder",
               description="Don't want to hold your frisbee? Don't!",
               cat_id="2", user_id="1")
session.add(newItem)
session.commit()

newItem = Item(title="Gloves",
               description="Butter fingers? Catch that frisbee easily!",
               cat_id="2", user_id="3")
session.add(newItem)
session.commit()

newItem = Item(title="ShinGuards",
               description="They'll stay here until you come back.",
               cat_id="2", user_id="2")
session.add(newItem)
session.commit()

newCategory = Category(name="Rugby")
session.add(newCategory)
session.commit()

newCategory = Category(name="Hockey")
session.add(newCategory)
session.commit()

newCategory = Category(name="Running")
session.add(newCategory)
session.commit()

newCategory = Category(name="Swimming")
session.add(newCategory)
session.commit()
