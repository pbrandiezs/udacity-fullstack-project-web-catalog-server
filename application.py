#!/usr/bin/env python

# Program: application.py
# Author: Perry Brandiezs
# Date: May 1, 2019
# Last Updated: May 6, 2019

# See the README.md at vagrant/catalog/README.md
# See the expected output document at vagrant/catalog/Expected_Output.docx


# This program demonstrates CRUD operations using an Item Catalog.

#   Create: Ability to create an airplane item
#   Read:   Ability to read an inventory list showing category name,
#       item name, item description.  Ability to show item detail, login
#       required.
#   Update: Ability to edit item detail, login required.
#   Delete: Ability to delete an item, login required and
#       must be item creator.

# This program demonstrates OAuth2 authentication and authorization using
#       a third party provider.
#   Login / Logout using Facebook is provided, link can be found at the
#       top-right of the main screen.
#   Login required to display item detail, update an item, or delete an item.
#   Must also be the item creator to delete.

# This program demonstrates API endpoints.
#   Display all items
#   Display specific item detail
#   Display all users
#   Display all categories


from flask import Flask, render_template, request, redirect, jsonify,\
    url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc
from sqlalchemy.orm import sessionmaker
from models import Base, User, ItemCatalog, Category
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import ssl


app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """ Create anti-forgery state token. """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    app_id = json.loads(open('fb_client_secrets.json', 'r').
                        read())['web']['app_id']
    return render_template('login.html', STATE=state, APP_ID=app_id)


def createUser(login_session):
    """ Helper function to create user. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """ Helper function to get user info. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """ Helper function to get user id from email. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except orm_exc.NoResultFound:
        return None


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """ Facebook OAuth2 login """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    # Exchange token for long-lived server-side token
    app_id = json.loads(open('fb_client_secrets.json', 'r').
                        read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').
                            read())['web']['app_secret']
    fb_url = ('https://graph.facebook.com/oauth/access_token'
              '?grant_type=fb_exchange_token&client_id=%s'
              '&client_secret=%s&fb_exchange_token=%s')
    url = fb_url % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace the
        remaining quotes with nothing so that it can be used directly in the
        graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')
    fb_url = ('https://graph.facebook.com/v2.8/me'
              '?access_token=%s&fields=name,id,email')
    url = fb_url % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    fb_url = ('https://graph.facebook.com/v2.8/me/picture'
              '?access_token=%s&redirect=0&height=200&width=200')
    url = fb_url % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]
    # see if user exists
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """ Facebook OAuth2 logout. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    fb_url = ('https://graph.facebook.com/%s/permissions'
              '?access_token=%s')
    url = fb_url % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/disconnect')
def disconnect():
    """ Disconnect session. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showItemCatalog'))
    else:
        flash("You were not logged in to begin with!")
        redirect(url_for('showItemCatalog'))


@app.route('/')
@app.route('/items/')
def showItemCatalog():
    """
    Show all Catalog Items.

    This is an example of CRUD: Read.
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categoriesanditems = session.query(
        Category, ItemCatalog).select_from(
        ItemCatalog).join(
        Category, Category.id == ItemCatalog.category_id)
    categoriesanditemsandusers = session.query(
        Category, ItemCatalog, User).select_from(
        ItemCatalog).join(
        Category, Category.id == ItemCatalog.category_id).join(
        User, User.id == ItemCatalog.user_id)
    # check if logged in
    if 'username' not in login_session:
        # not logged in, display public items
        return render_template('publicitems.html',
                               categoriesanditems=categoriesanditems)
    else:
        # logged in, display items (including creator)
        return (
                render_template(
                    'items.html',
                    categoriesanditemsandusers=categoriesanditemsandusers))


@app.route('/item/new/', methods=['GET', 'POST'])
def newItem():
    """
    Create a new item.

    This is an example of CRUD: Create.
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        category_name = request.form['category_name']
        NewCategory = Category(category_name=category_name)
        try:
            session.add(NewCategory)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
        new_category_id = session.query(Category.id).filter_by(
                                        category_name=category_name)
        newItem = ItemCatalog(
                    category_id=new_category_id,
                    item_name=request.form['item_name'],
                    item_description=request.form['item_description'],
                    user_id=login_session['user_id'])
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.item_name)
        session.commit()
        return redirect(url_for('showItemCatalog'))
    else:
        return render_template('newItem.html')


@app.route('/item/<int:id>/edit/', methods=['GET', 'POST'])
def editItem(id):
    """
    Edit an item.

    This is an example of CRUD: Update.
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        # not logged in, display public items
        flash("Login required to edit!")
        return redirect(url_for('showItemCatalog'))
    editedItem = session.query(ItemCatalog).filter_by(id=id).one_or_none()
    if editedItem is None:
        flash("Item does not exist!")
        return redirect(url_for('showItemCatalog'))
    categoriesanditems = session.query(
        Category, ItemCatalog).filter(
        ItemCatalog.id == id).join(
        Category, Category.id == ItemCatalog.category_id).one()
    if editedItem.user_id != login_session['user_id']:
        flash(
              "Not authorized to edit this item!  "
              "Create your own item to edit.")
        return redirect(url_for('showItemCatalog'))
    if request.method == 'POST':
        if (request.form['item_name'] and request.form['category_name'] and
                request.form['item_description']):
            category_name = request.form['category_name']
            NewCategory = Category(category_name=category_name)
            try:
                session.add(NewCategory)
                session.commit()
            except exc.IntegrityError:
                session.rollback()
            editedItem.item_name = request.form['item_name']
            editedItem.item_description = request.form['item_description']
            session.add(editedItem)
            session.commit()
            return redirect(url_for('showItemCatalog'))
    else:
        return (
            render_template('editItem.html',
                            categoriesanditems=categoriesanditems))


@app.route('/item/<int:id>/delete/', methods=['GET', 'POST'])
def deleteItem(id):
    """
    Delete an item.

    This is an example of CRUD: Delete.
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    itemToDelete = session.query(ItemCatalog).filter_by(id=id).one()
    # check if logged in
    if 'username' not in login_session:
        # not logged in, display public items
        flash("Login required to delete!")
        return redirect(url_for('showItemCatalog'))
    if itemToDelete.user_id != login_session['user_id']:
        flash("Not authorized to delete this item!  "
              "Create your own item to delete.")
        return redirect(url_for('showItemCatalog'))
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.item_name)
        session.commit()
        return redirect(url_for('showItemCatalog'))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


@app.route('/item/<int:item_id>/')
def showItem(item_id):
    """
    Show an item.

    An example of CRUD: Read
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(ItemCatalog).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    items = session.query(ItemCatalog).filter_by(id=ItemCatalog.id).all()
    username = session.query(User.username).filter_by(id=creator.id).one()
    categoriesanditems = session.query(
        Category, ItemCatalog).filter(
        ItemCatalog.id == item_id).join(
        Category, Category.id == ItemCatalog.category_id).one()
    category_name = categoriesanditems.Category.category_name
    # Check if logged in
    if 'username' not in login_session:
        flash('Must log in to view item detail!')
        return redirect(url_for('showItemCatalog'))
    else:
        return (render_template('item.html',
                item=item,
                username=username[0],
                category_name=category_name))


@app.route('/items/JSON')
def itemsJSON():
    """ JSON endpoint to show all items. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(ItemCatalog).all()
    return jsonify(items=[item.serialize for item in items])


@app.route('/item/<int:item_id>/JSON')
def itemJSON(item_id):
    """ JSON endpoint to show a specific item. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(ItemCatalog).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    items = session.query(ItemCatalog).filter_by(id=ItemCatalog.id).all()
    username = session.query(User.username).filter_by(id=creator.id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    # Check if logged in
    if 'username' not in login_session:
        # not logged in
        return jsonify({"item": [
            {
                "category_id": item.category_id,
                "category_name": category.category_name,
                "id": item.id,
                "item_description": item.item_description,
                "item_name": item.item_name,
            }]
        })
    else:
        # logged in, include creator with the result
        return jsonify({"item": [
            {
                "category_id": item.category_id,
                "category_name": category.category_name,
                "id": item.id,
                "item_description": item.item_description,
                "item_name": item.item_name,
                "creator": username[0]
            }]
        })


@app.route('/users/JSON')
def usersJSON():
    """ JSON endpoint to show all users. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    users = session.query(User).all()
    return jsonify(users=[user.serialize for user in users])


@app.route('/categories/JSON')
def categoriesJSON():
    """ JSON endpoint to show all categories. """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


if __name__ == '__main__':
    """ Main run web server using port 8000. """
    app.secret_key = 'super_secret_key'
    app.debug = True
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context = ('ssl.cert', 'ssl.key')
    app.run(host='0.0.0.0',
            port=8000,
            ssl_context=context,
            threaded=True,
            debug=True)
