from http import client
from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'\xe9!\xbd\x8f\xfc\x8e\xf6\xb7^\xdb\xd5S\x8cP\xf7U'

#Database connection
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login

from user import routes

#decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")
    return wrap


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html', budgets=session['user']["data"])