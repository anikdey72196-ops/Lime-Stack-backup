# This file is names __init__.py because that's how flask recognises, this is a package
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Fetch the secret keys from the environment variables
# Note: Ensure your .env file has SECRET_KEY=your_secret and JWT_SECRET_KEY=your_jwt_secret
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key_if_not_found')

# It is recommended to use a separate secret key for JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_if_not_found')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)

from app import routes
