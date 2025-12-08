from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
from app.forms import SignInForm, SignUpForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('main.home'))


@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/archive')
@login_required
def archive():
    return render_template('archive.html')


@main.route('/signin', methods=['GET', 'POST'])
def SignIn():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Signed in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('signin.html', form=form)


@main.route('/signup', methods=['GET', 'POST'])
def SignUp():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please sign in.', 'success')
        return redirect(url_for('main.SignIn'))
    
    return render_template('signup.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('main.home'))
