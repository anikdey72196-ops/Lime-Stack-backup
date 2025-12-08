from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, bcrypt, db
from app.forms import LoginForm, PostForm, RegistrationForm
from app.models import Post, User

#login_user is a function to log the user in


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/SignIn", methods=['GET', 'POST'])
def SignIn():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user)  # it is a true false based data
            return redirect(url_for('archive'))
        flash('Login Unsuccessful, Please check email and password')
    print(form.errors)
    return render_template("SignIn.html", title='Login', form=form)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('archive'))
    forms = RegistrationForm()
    if forms.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(forms.password.data)
        #database entry
        user = User(username=forms.username.data,
                    email=forms.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created !", 'success')
        return redirect(url_for('SignIn'))
    print(forms.errors)
    return render_template("registration.html", title='Register', form=forms)


@app.route("/archive", methods=['GET', 'POST'])
def archive():
    posts = Post.query.all()
    return render_template("archive.html", posts=posts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/post/new", methods=['GET', 'POST'])
@login_required  #Use login_required as a decorator not a function
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user)  #author is backref connected to Post class
        db.session.add(post)
        db.session.commit()
        print(form.errors)
        flash("You post has been submited")
        return redirect(url_for('archive'))
    return render_template('createPost.html',
                           title='Create New Post',
                           form=form)
