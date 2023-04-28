"""Provide controllers for all routes populated with model data."""
from datetime import datetime

import pytz
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    """Home page for blog.

    Returns:
    -------
        str: HTML generated from index.html Jinja template filled with posts.
    """
    posts = [
        {
            "author": {"username": "Joey"},
            "title": "CSP",
            "body": "This card is great to use!",
        },
        {
            "author": {"username": "Joey"},
            "title": "CFU",
            "body": "This card is versatile!",
        },
    ]
    return render_template("index.html", title="Home", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page for registered users.

    Returns:
    -------
        str: HTML generated from login.html Jinja template filled with LoginForm.
    """
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc:
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    """Log out a logged in user and redirect the user to the Home page.

    Returns:
    -------
        str: HTML for Home page.
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/secret")
def secret():
    """Secret page.

    Returns:
    -------
        str: HTML generated from secret Jinja Template.
    """
    return render_template("index.html", title="Secret Page")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration page for registering a new user.

    Returns:
    -------
        str: HTML generated from register.html Jinja template filled with
             RegistrationForm.
    """
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)  # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username: str):
    """Profile page for registered users.

    Keyword Arguments:
    -----------------
        username (str): username of user's profile page.

    Returns:
    -------
        str: HTML generated from user.html Jinja template filled with a user's
             username and posts.
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "test post 1"},
        {"author": user, "body": "test post 2"},
    ]
    return render_template("user.html", user=user, posts=posts)


@app.before_request
def before_request():
    """Log a logged in user's last seen time in UTC."""
    if current_user.is_authenticated:  # type: ignore
        current_user.last_seen = datetime.now(pytz.utc)
        db.session.commit()


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Profile editing page for a logged in user to edit their user profile.

        On valid form submit data is copied to user object and written to db.
        When submit is invalid this is due to 2 reasons. One, the page is
        requested for first time with GET request so the form is populated with
        db data. Otherwise, there is a validation error from the data submitted
        in the form and form is left unchanged.

    Returns:
    -------
        str: HTML generated from edit_profile.html Jinja template filled with
             EditProfileForm.
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username  # type: ignore
        form.about_me.data = current_user.about_me  # type: ignore
    return render_template("edit_profile.html", title="Edit Profile", form=form)
