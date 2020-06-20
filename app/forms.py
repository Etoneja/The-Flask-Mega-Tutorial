from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import data_required, ValidationError, length


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

