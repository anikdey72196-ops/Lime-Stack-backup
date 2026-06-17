# This file is names __init__.py because that's how flask recognises, this is a package
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '1fec41ec87124ae865fad317fbff8871'
# It is recommended to use a separate secret key for JWT
app.config['JWT_SECRET_KEY'] = '1fec41ec87124ae865fad317fbff8871'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)

from app import routes
