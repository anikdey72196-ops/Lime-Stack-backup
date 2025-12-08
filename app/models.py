
from datetime import datetime

from app import db

from app import login_manager
from flask_login import UserMixin 

#UserMixin contains all the methods and the attributes
# we need to set the work with the user_loader extension


# login session manager
@login_manager.user_loader  # setting up the user_loader extension to load the user
def load_user(user_id):     #using user_id to load the user
    return User.query.get(int(user_id))



#To reloading the session of the logged in user, we need to create a decorator function


'''
# This is what db.Model does "under the hood"
def __init__(self, **kwargs):
    for key, value in kwargs.items():
        setattr(self, key, value)

'''
# This contains all the personal info of the user
class User(db.Model, UserMixin):   #creating class User for the db.model inheritance
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    email = db.Column(db.String(20), unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post', backref='author',lazy=True) 
    # first entry in the class you want to build the relatiobship with


    def __repr__(self):
        return f"User({self.username},{self.email},{self.image_file})"  
    #User just used as a string nothing special here ## don't forget the classic rules



class Post(db.Model):  # Gonna contain all the user written posts
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)  
    # in user.id, user's u is smaller case cause we ain't calling the whole User class
    # the table name which by defaults to smaller case of the class name, here it will 
    #be just 'user'

    def __repr__(self):   #here inheritance won't work cause defined functions only supports instance
        return f"Posts({self.title},{self.date_posted})"

