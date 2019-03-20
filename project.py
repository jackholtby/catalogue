from flask import Flask

app = Flask(__name__)

# Show main Catalogue page
@app.route('/')
@app.route('/catalogue')
def showCatalogue():
    output = "<p>The Catalogue's main page</p>"
    return output

# Show items inside specific category
@app.route('/catalogue/<int:category_id>')
@app.route('/catalogue/<int:category_id>/items/')
def showCategory(category_id):
    output = "The page for category with id: %s" category_id
    return output

# Edit a category
@app.route('/catalogue/<int:category_id>/edit/')
def editCategory(category_id):
    output = "The page for editing category with id: %s" category_id
    return output

# Delete a category
@app.route('/catalogue/<int:category_id>/delete/')
def deleteCategory(category_id):
    output = "The page for deleting category with id: %s" category_id
    return output

# Show item
@app.route('/catalogue/<int:category_id>/<int:item_id>/')
def showItem(item_id):
    output = "The page for showing item with id: %s" item_id
    return output

# Edit item
@app.route('/catalogue/<int:category_id>/<int:item_id>/edit/')
def editItem(item_id):
    output = "The page for editing item with id: %s" item_id
    return output

# Delete item
@app.route('/catalogue/<int:category_id>/<int:item_id>/delete/')
def deleteItem(item_id):
    output = "The page for deleting item with id: %s" item_id
    return output

@app.route('/catalogue.json')
def json():
    output = "This is where you'd see the JSON endpoint data."
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
