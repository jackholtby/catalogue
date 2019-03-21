from flask import Flask

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show main Catalogue page
@app.route('/')
@app.route('/catalogue/')
def showCatalogue():
    return "The Catalogue's main page"

# Show category and items contained within it
@app.route('/catalogue/<int:category_id>/')
@app.route('/catalogue/<int:category_id>/items/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return "The page for category with id: %s" % category.id

# Create a category
@app.route('/catalogue/new/')
def newCategory():
    return "The page for creating a new category"

# Edit a category
@app.route('/catalogue/<int:category_id>/edit/')
def editCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return "The page for editing category with id: %s" % category.id

# Delete a category
@app.route('/catalogue/<int:category_id>/delete/')
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return "The page for deleting category with id: %s" % category.id

# Show item
@app.route('/catalogue/<int:category_id>/<int:item_id>/')
def showItem(item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(cat_id=category.id, id=item_id).one()
    return "The page for showing item with id: %s" % item.id

# Create item
@app.route('/catalogue/<int:category_id>/new/')
def newItem(category_id):
    return "The page for creating a new item"

# Edit item
@app.route('/catalogue/<int:category_id>/<int:item_id>/edit/')
def editItem(item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return "The page for editing item with id: %s" % item.id

# Delete item
@app.route('/catalogue/<int:category_id>/<int:item_id>/delete/')
def deleteItem(item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return "The page for deleting item with id: %s" % item.id

@app.route('/catalogue.json')
def json():
    return "This is where you'd see the JSON endpoint data."

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
