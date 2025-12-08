from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=19)])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me ?')
    



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max= 10)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=19)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    remember_me = BooleanField('Remember Me ?')
    #custom validators
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken, please try a different username')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exists, please try a different username')
        

class PostForm(FlaskForm):  # to create new post in archives
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=50)])
    submit = SubmitField('submit')

