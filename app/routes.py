from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def main():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"username:  {form.username.data}; remember_me: {form.remember_me.data}")
        return redirect(url_for("main"))
    return render_template("login.html", form=form)
