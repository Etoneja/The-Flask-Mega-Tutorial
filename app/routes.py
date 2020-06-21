from flask import (
    render_template, flash, redirect, url_for, request
)
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from app.forms import (
    LoginForm, RegistrationForm, EditProfileForm, EmptyForm, NewPostForm
)
from flask.blueprints import Blueprint
from werkzeug.urls import url_parse
from datetime import datetime

from app.database import db
from app.models import User, Post
from app import app

blog = Blueprint(
    'blog', __name__,
    template_folder='../templates',
    static_folder='static'
)


@blog.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@blog.route("/", methods=["GET", "POST"])
@blog.route("/index", methods=["GET", "POST"])
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    form = NewPostForm()

    if form.validate_on_submit():
        p = Post(body=form.body.data, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash("Post created!")
        return redirect(url_for("blog.index"))
    prev_page_url = url_for("blog.index", page=posts.prev_num) if posts.has_prev else None
    next_page_url = url_for("blog.index", page=posts.next_num) if posts.has_next else None
    return render_template(
        "index.html",
        title="Index",
        posts=posts.items,
        form=form,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url
    )


@blog.route("/subscriptions", methods=["GET"])
@login_required
def subscriptions():
    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )

    prev_page_url = url_for("blog.subscriptions", page=posts.prev_num) if posts.has_prev else None
    next_page_url = url_for("blog.subscriptions", page=posts.next_num) if posts.has_next else None
    return render_template(
        "index.html",
        title="Index",
        posts=posts.items,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url
    )


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
@login_required
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


@blog.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template("profile.html", title="Profile", user=user, form=form)


@blog.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about = form.about.data
            db.session.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("blog.profile", username=current_user.username))

    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about.data = current_user.about

    return render_template("edit_profile.html", form=form)


@blog.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} not found.")
            return redirect(url_for("blog.index"))
        if user == current_user:
            flash("You can not follow yourself")
            return redirect(url_for("blog.profile", username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f"Followed {username}!")
        return redirect(url_for("blog.profile", username=username))
    return redirect(url_for("blog.index"))


@blog.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} not found.")
            return redirect(url_for("blog.index"))
        if user == current_user:
            flash("You can not unfollow yourself")
            return redirect(url_for("blog.profile", username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f"Unfollowed {username}!")
        return redirect(url_for("blog.profile", username=username))
    return redirect(url_for("blog.index"))
