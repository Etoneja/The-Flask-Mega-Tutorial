from flask import render_template

from app import app
from app.database import db


@app.errorhandler(404)
def error_404(error):
    return render_template("error_404.html"), 404


@app.errorhandler(500)
def error_500(error):
    db.session.rollback()
    return render_template("error_500.html"), 500
