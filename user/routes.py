from app import app
from user.models import User

@app.route('/user/signup/', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/login/', methods=['POST'])
def login():
    return User().login()

@app.route('/user/signout/')
def signout():
    return User().signout()

@app.route('/user/create_budget/', methods=['POST'])
def create_budget():
    return User().create_budget()

@app.route('/user/add_transaction/', methods=['POST'])
def add_transaction():
    return User().add_transaction()
