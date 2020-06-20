from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import (
    data_required, ValidationError, Length, Email, EqualTo
)
from flask_login import current_user

from app.models import User


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[
        data_required(),
        Length(min=3)
    ])
    password = PasswordField("Password", validators=[
        data_required(),
        Length(min=3)
    ])
    remember_me = BooleanField("Remember me", default=True)
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[
        data_required(),
        Length(min=3)
    ])
    email = StringField("Email", validators=[
        data_required(),
        Email(),
        Length(min=3, max=120)
    ])
    password = PasswordField("Password", validators=[
        data_required(),
        Length(min=3)
    ])
    password_2 = PasswordField("Confirm password", validators=[
        data_required(),
        Length(min=3),
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


class EditProfileForm(FlaskForm):

    username = StringField("Username", validators=[
        data_required(),
        Length(min=3)
    ])
    email = StringField("Email", validators=[
        data_required(),
        Email(),
        Length(min=3)
    ])
    about = TextAreaField("About", validators=
        [Length(max=200)]
    )
    submit = SubmitField("Submit changes")

    @staticmethod
    def validate_username(form, username):
        u = User.query.filter_by(username=username.data).first()
        if u is not None and u.username != current_user.username:
            raise ValidationError("User exists")

    @staticmethod
    def validate_email(form, email):
        e = User.query.filter_by(email=email.data).first()
        if e is not None and e.email != current_user.email:
            raise ValidationError("Email dupe")
