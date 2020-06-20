from flask import render_template, flash, redirect, url_for
from flask.blueprints import Blueprint
from app.forms import LoginForm
from app.database import db
from app.models import User, Post


blog = Blueprint(
    'blog', __name__,
    template_folder='../templates',
    static_folder='static'
)


@blog.route("/")
@blog.route("/index")
def main():
    posts = Post.query.all()
    return render_template("main.html", posts=posts)


@blog.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"username:  {form.username.data}; remember_me: {form.remember_me.data}")
        return redirect(url_for("blog.main"))
    return render_template("login.html", form=form)
