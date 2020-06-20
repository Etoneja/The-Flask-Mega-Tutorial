from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    data_required, ValidationError, length, Email, EqualTo
)

from app.models import User


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[
        data_required(),
        length(min=3)
    ])
    password = PasswordField("Password", validators=[
        data_required(),
        length(min=3)
    ])
    remember_me = BooleanField("Remember me", default=True)
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[
        data_required(),
        length(min=3)
    ])
    email = StringField("Email", validators=[
        data_required(),
        Email(),
        length(min=3, max=120)
    ])
    password = PasswordField("Password", validators=[
        data_required(),
        length(min=3)
    ])
    password_2 = PasswordField("Confirm password", validators=[
        data_required(),
        length(min=3),
        EqualTo("password")
    ])
    submit = SubmitField("Sign up")

    @staticmethod
    def validate_username(form, username):
        u = User.query.filter_by(username=username.data).first()
        if u is not None:
            raise ValidationError("User exists")

    @staticmethod
    def validate_email(form, email):
        e = User.query.filter_by(email=email.data).first()
        if e is not None:
            raise ValidationError("Email dupe")
