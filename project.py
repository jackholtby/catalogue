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
@app.route('/catalogue')
def showCatalogue():
    output = "<p>The Catalogue's main page</p>"
    return output

# Show items inside specific category
@app.route('/catalogue/<int:category_id>/')
@app.route('/catalogue/<int:category_id>/items/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    return "The page for category with id: %s" % category

# Edit a category
@app.route('/catalogue/<int:category_id>/edit/')
def editCategory(category_id):
    return "The page for editing category with id: %s" % category_id

# Delete a category
@app.route('/catalogue/<int:category_id>/delete/')
def deleteCategory(category_id):
    return "The page for deleting category with id: %s" % category_id

# Show item
@app.route('/catalogue/<int:category_id>/<int:item_id>/')
def showItem(item_id):
    return "The page for showing item with id: %s" % item_id

# Edit item
@app.route('/catalogue/<int:category_id>/<int:item_id>/edit/')
def editItem(item_id):
    return "The page for editing item with id: %s" % item_id

# Delete item
@app.route('/catalogue/<int:category_id>/<int:item_id>/delete/')
def deleteItem(item_id):
    return "The page for deleting item with id: %s" % item_id

@app.route('/catalogue.json')
def json():
    return "This is where you'd see the JSON endpoint data."

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
