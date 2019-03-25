from flask import Flask, render_template

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
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('categories.html', categories = categories, items = items)

# Show category and items contained within it
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).all()
    return render_template('category.html', category = category, items = items)

# Create a category
@app.route('/category/new/')
def newCategory():
    return render_template('newCategory.html')

# Edit a category
@app.route('/category/<int:category_id>/edit/')
def editCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('editCategory.html', category = category)

# Delete a category
@app.route('/category/<int:category_id>/delete/')
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('deleteCategory.html', category = category)

# Show item
@app.route('/category/<int:category_id>/<int:item_id>/')
def showItem(item_id, category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(cat_id=category.id, id=item_id).one()
    return render_template('item.html', category = category, item = item)

# Create item
@app.route('/category/<int:category_id>/new/')
def newItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('newItem.html', cat_id = category)

# Edit item
@app.route('/category/<int:category_id>/<int:item_id>/edit/')
def editItem(item_id, category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(cat_id=category_id, id=item_id).one()
    return render_template('editItem.html', category = category, item = item)

# Delete item
@app.route('/category/<int:category_id>/<int:item_id>/delete/')
def deleteItem(item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return "The page for deleting item with id: %s" % item.id

@app.route('/catalogue.json')
def json():
    return "This is where you'd see the JSON endpoint data."

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)
