# This file is names __init__.py because that's how flask recognises, this is a package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # for hashing passwords
from flask_login import LoginManager #to manage Sign In services



app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '1fec41ec87124ae865fad317fbff8871'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app) #passing app in the loging manager


from app import routes  #because in the routes file the route will work after this line