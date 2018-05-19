#shebang line for python 2
#!/usr/bin/env python
# nessary module for this app
from flask import (Flask, render_template, redirect, url_for, jsonify,
                   request, flash, make_response)
from database_setup import Base, Catogrey, Branche, User, UserBranche
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import random
import string
import httplib2
import requests
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

CLIENT_ID = """424450135644-mr562q0qr5h9a2aiagr4b7skvj13mgv6.
               apps.googleusercontent.com"""
APP_NAME = "Restaurant Menu app"
# initalize the app
app = Flask(__name__)
# connecting to database the created
engine = create_engine("sqlite:///catogrey.db")
Base.metadata.bind = engine
dbsesstion = sessionmaker(bind=engine)
session = dbsesstion()

""" this function take the item and return the name of the catogrey the item
belong to it"""


def get_catogrey(item):
    # catogries=session.query(Catogrey).all();
    catogrey = session.query(Catogrey).filter_by(id=item.catogrey_id).one()
    return catogrey.name

""" default  hompage if  user  not  loged in  its display the  default items if 
user loged in its display the user own branches """


@app.route("/")
@app.route("/index")
@app.route("/home")
def homepage():
    catogreies = session.query(Catogrey).all()

    if 'username' in login_session:
        items = session.query(UserBranche).all()
        return render_template("home.html", catogreies=catogreies, items=items,
                               get_catogrey=get_catogrey)

    elif 'username' not in login_session:
        items = session.query(Branche).all()
        return render_template(
            "publichome.html",
            catogreies=catogreies,
            items=items,
            get_catogrey=get_catogrey)

# this function display branches of the selected catogrey with it id
# also when user not loged in display publicdescription.htm others
# displayes the description.html


@app.route("/catogrey/<int:id>/branches")
def catogrey_branches(id):

    catogrey = session.query(Catogrey).filter_by(id=id).one()
    catogries = session.query(Catogrey).all()
    if 'username' in login_session:
        branches = session.query(UserBranche).filter(
            and_(catogrey_id=id, user_id=login_session['user_id']))
        counter = 0
        for i in branches:
            counter += 1
        return render_template(
            'catogrey.html',
            catogries=catogries,
            catogrey=catogrey,
            branches=branches,
            counter=counter)
    elif 'username' not in login_session:
        branches = session.query(Branche).filter_by(catogrey_id=id)
        counter = 0
        for i in branches:
            counter += 1
        return render_template(
            'publiccatogrey.html',
            catogries=catogries,
            catogrey=catogrey,
            branches=branches,
            counter=counter)


""""this function displayed the description of selected branche when user loged
in display description.html other display publicdescription.html
"""


@app.route("/catogrey/branche/<int:id>/description")
def getBranchDescription(id):
    # item=session.query(Branche).filter_by(id=id).one();
    if 'username' in login_session:
        item = session.query(UserBranche).filter(
            and_(id=id, user_id=login_session['user_id'])).one()

        return render_template('description.html', item=item)
    else:
        item = session.query(Branche).filter_by(id=id).one()
        return render_template('publicdescription.html', item=item)


""""
allowed only fir loged in users
this save changes od edit ranche on database after user press the button
other render the template that enable the edit process
"""


@app.route("/catogrey/brance/<int:id>/edit", methods=["POST", "GET"])
def editBranche(id):
    item = session.query(UserBranche).filter(
        and_(id=id, user_id=login_session['user_id'])).one()

    if request.method == "POST":
        if request.form.get('name'):
            item.name = request.form.get('name')
            # print item.name;
        if request.form.get('description'):
            item.description = request.form.get('description')
            # print item.description
        if request.form.get('catogrey'):
            # print request.form.get('catogrey');
            element = session.query(Catogrey).filter_by(
                name=request.form.get('catogrey')).one()
            item.catogrey_id = element.id
        session.commit()
        flash("%s Successfully edited" % item.name)
        return redirect(url_for('homepage'))
    else:
        catogries = session.query(Catogrey).all()
        return render_template('editbranche.html', catogries=catogries)


"""
allowed only for loged in user
this function render emplate that enable delete process
and save changes to database after user press button
"""


@app.route("/catogrey/branche/<int:id>/delete", methods=["POST", "GET"])
def deleteBranche(id):
    item = session.query(UserBranche).filter(
        and_(id=id, user_id=login_session['user_id'])).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        # items=session.query(Branche).all();
        # catogries=session.query(Catogrey).all();
        # return
        # render_template('home.html',items=items,catogries=catogries,get_catogrey=get_catogrey);
        return redirect(url_for('homepage'))
    else:
        # catogries=session.query(Catogrey).all();
        return render_template('deletebranche.html', item=item)


"""
allowed only for loged in users
this function enable the user to create new branche and save it to database
"""


@app.route("/branche/new/", methods=["POST", "GET"])
def create_branche():
    if request.method == "POST":
        cat_id = session.query(Catogrey).filter_by(
            name=request.form.get('catogrey')).one()
        item = UserBranche(
            name=request.form['name'],
            description=request.form['description'],
            catogrey_id=cat_id.id,
            user_id=login_session['user_id'])
        session.add(item)
        session.commit()
        items = session.query(Branche).all()
        catogries = session.query(Catogrey).all()
        # return render_template('home.html', items=items,
        # catogries=catogries,get_catogrey=get_catogrey);
        return redirect(url_for("homepage"))
    else:
        catogries = session.query(Catogrey).all()
        return render_template('newbranche.html', catogries=catogries)


"""
allowed for loged in user
this function allowe loged in user to display branches they created in json
format
"""


@app.route("/branches/json")
def branchesJson():
    branches = session.query(UserBranche).all()
    return jsonify(Branches=[i.serialize for i in branches])


"""
allowed for loged in users
display the catogries in json format
"""


@app.route("/catogries/json")
def catogriesJson():
    catogries = session.query(Catogrey).all()
    return jsonify(Catogries=[i.serialize for i in catogries])


"""
display the login template to enale user authentication
"""


@app.route("/login")
def showlogin():
    state = "".join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "the current state is:"+state;
    return render_template('login.html', STATE=state)


"""
this function is invoked when user loged in with it google account
"""


@app.route('/gconnect')
def gconnect():
    if request.args.date() != login_session['state']:
        response = make_response(json.dumps("State not Match"))
        response.headers['Content-Type'] = 'application/json'
        return response
    data = request.get['data']
    code = data.dcode('utf-8')
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = "postmessage"
        credentails = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps("There Is an error will exchange The Code"))
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentails.access_token()
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = h.request(url, "GET")[1]
    result = json.loads(result.decode('utf-8'))
    if result.get('error') is not None:
        response = make_response("error To Get Information From Google")
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentails.id_token['sub']
    if result['gplus_id'] != gplus_id:
        response = make_response("Error In Google Plus Id")
        response.headers['Content-Type'] = 'application.json'
        return response
    if result['isused_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("The Use Of Code Not applicable For Thos app"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and stored_gplus_id == gplus_id:
        response = make_response(json.dumps("ok now the user connected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answers = requests.get(userinfo_url, params=params)
    data = answers.json()
    login_session['name'] = data['username']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserId(login_session['email'])
    if user_id is None:
        newuser = createUser(login_session)
    login_session['user_id'] = newuser
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    return output


"""thi function used to add the user authinticated for first time
to be add to database
"""


def createUser(login_session):
    user = User(
        name=login_session['username'],
        picture=login_session['picture'],
        email=login_session['email'])
    session.add(user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


"""
this function return the user info if user found
"""


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


"""
this function get the user id fron his own email
"""


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


"""
this function loged the user out invoked when user press on logout
"""


@app.route('/gdicconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps("You are areldy logged out"), 501)
        response.headers['Content-Type'] = 'application/json'
        return response
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['gplus_id']
    del login_session['access_token']
    response = make_response(json.dumps("Successfully Loged Out"), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


"""
display the app and run it
"""
if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
