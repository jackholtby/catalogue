from flask import Flask, render_template, request, redirect, url_for

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
@app.route('/category/<string:category_name>/')
@app.route('/category/<string:category_name>/items/')
def showCategory(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(cat_id=category.id).all()
    return render_template('category.html', categories = categories, category = category, items = items)

# Show item
@app.route('/category/<string:category_name>/<string:item_name>/')
def showItem(item_name, category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(cat_id=category.id, title=item_name).one()
    return render_template('item.html', category = category, item = item)

# Create item
@app.route('/item/new/', methods=['GET', 'POST'])
def newItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(title = request.form['title'],
                       description = request.form['description'],
                       cat_id = request.form['category'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCatalogue'))
    else:
        return render_template('newItem.html', categories = categories)

# Edit item
@app.route('/category/<string:category_name>/<string:item_name>/edit/', methods=['POST', 'GET'])
def editItem(item_name, category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    editedItem = session.query(Item).filter_by(cat_id= category.id, title=item_name).one()
    if request.method == 'POST':
        editedItem.title = request.form['title']
        editedItem.description = request.form['description']
        editedItem.cat_id = request.form['category']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showCatalogue'))
    else:
        return render_template('editItem.html', categories = categories, category = category, item = editedItem)

# Delete item
@app.route('/category/<string:category_name>/<string:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    itemToDelete = session.query(Item).filter_by(cat_id=category.id, title=item_name).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCatalogue'))
    else:
        return render_template('deleteItem.html', category = category, item = itemToDelete)

# Login
@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/catalogue.json')
def json():
    return "This is where you'd see the JSON endpoint data."

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)
