from flask import (
    render_template, flash, redirect, url_for, request
)
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from flask.blueprints import Blueprint
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm
from app.database import db
from app.models import User, Post


blog = Blueprint(
    'blog', __name__,
    template_folder='../templates',
    static_folder='static'
)


@blog.route("/")
@blog.route("/index")
@login_required
def index():
    posts = Post.query.all()
    return render_template("index.html", title="Index", posts=posts)


@blog.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("blog.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No such user or invalid password.")
            return redirect(url_for("blog.login"))
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("blog.index")
        login_user(user, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template("login.html", title="sign-in", form=form)


@blog.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("blog.login"))


@blog.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("blog.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulation, you are now a registered user!")
        return redirect(url_for("blog.index"))
    return render_template("signup.html", title="sign-up", form=form)
