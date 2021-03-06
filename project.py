from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   jsonify,
                   make_response)
from flask import session as login_session
from oauth2client.client import (flow_from_clientsecrets,
                                 FlowExchangeError)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import (Base,
                            Category,
                            Item,
                            User)
import random
import string
import httplib2
import requests
import json

# What's in a name!?
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalogue"

# Connect to the database
engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show main Catalogue page
@app.route('/')
@app.route('/category/')
def showCatalogue():
    categories = session.query(Category).all()
    items = session.query(Item).all()

    # Check if user is logged in, if not, show public main page.
    if 'username' not in login_session:
        return render_template('publicCategories.html',
                               categories=categories, items=items)
    else:
        return render_template('categories.html',
                               categories=categories, items=items)


# Show category and items contained within it
@app.route('/category/<string:category_name>/')
@app.route('/category/<string:category_name>/items/')
def showCategory(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(cat_id=category.id).all()
    if 'username' not in login_session:
        return render_template('publicCategory.html', categories=categories,
                               category=category, items=items)
    else:
        return render_template('category.html', categories=categories,
                               category=category, items=items)


# Show item
@app.route('/category/<string:category_name>/<string:item_name>/')
def showItem(item_name, category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(cat_id=category.id,
                                         title=item_name).one()
    # Check if user is logged in, and if they created the current item.
    creator = getUserInfo(item.user_id)

    # Check if user is logged in or own the item. Redirect to login if not.
    if 'username' not in login_session \
            or creator.id != login_session['user_id']:
        return render_template('publicItem.html', category=category, item=item)
    else:
        return render_template('item.html', category=category, item=item)


# Create item
@app.route('/item/new/', methods=['GET', 'POST'])
def newItem():
    # Check if user is logged in. Redirect to login if not.
    if 'username' not in login_session:
        return redirect('/login/')
    else:
        # Get list of categories
        categories = session.query(Category).all()

        # Create that item
        if request.method == 'POST':
            newItem = Item(title=request.form['title'],
                           description=request.form['description'],
                           cat_id=request.form['category'],
                           user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            return redirect(url_for('showCatalogue'))
        else:
            return render_template('newItem.html', categories=categories)


# Edit item
@app.route('/category/<string:category_name>/<string:item_name>/edit/',
           methods=['POST', 'GET'])
def editItem(item_name, category_name):
    # Get list of categories, get current category and item.
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    editedItem = session.query(Item).filter_by(cat_id=category.id,
                                               title=item_name).one()
    creator = getUserInfo(editedItem.user_id)

    # Check if user is logged in or own the item. Redirect to login if not.
    if 'username' not in login_session \
            or creator.id != login_session['user_id']:
        return redirect('/login/')
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not \
            authorized to edit this item. Make your own item to edit.')} \
            </script><body onload='myFunction()'>"

    # Edit that item
    if request.method == 'POST':
        editedItem.title = request.form['title']
        editedItem.description = request.form['description']
        editedItem.cat_id = request.form['category']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showCatalogue'))
    else:
        return render_template('editItem.html', categories=categories,
                               category=category, item=editedItem)


# Delete item
@app.route('/category/<string:category_name>/<string:item_name>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    # Check if user is logged in. Redirect to login if not.
    if 'username' not in login_session:
        return redirect('/login/')
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not \
            authorized to edit this item. Make your own item to edit.')} \
            </script><body onload='myFunction()'>"

    # Get current item and category
    category = session.query(Category).filter_by(name=category_name).one()
    itemToDelete = session.query(Item).filter_by(cat_id=category.id,
                                                 title=item_name).one()

    # Delete that item
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCatalogue'))
    else:
        return render_template('deleteItem.html', category=category,
                               item=itemToDelete)


# Google Sign-in Server Side Function
# This is the code that Udacity provided in their course. If you can tell
# me how to get the thing working, please do.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data.get('name', '')
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Make a new user IF the user doesn't exist in the database yet.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:'
    output += '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Google Disconnect
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('User not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
    url = url % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps("Couldn't revoke token for.", 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Login
@app.route('/login/')
def showLogin():
    # Variable identify current login session
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', CLIENT_ID=CLIENT_ID)

# User account helper functions


# Create a new user
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
            email=login_session['email']).one_or_none()
    return user.id


# Get some info about the user
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Get user ID
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


# Output the JSON endpoint data
@app.route('/catalogue.json')
def json():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return jsonify(categories=[r.serialize for r in categories])


# Single Item json page
@app.route('/category/<string:category_name>/<string:item_name>/json/')
def jsonItem(category_name, item_name):
    # Get current item and category
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(cat_id=category.id,
                                         title=item_name).one()
    return jsonify(item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
