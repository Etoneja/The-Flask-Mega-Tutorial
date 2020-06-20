from flask_login import LoginManager

from app.models import User


login = LoginManager()
login.login_view = "blog.login"


@login.user_loader
def load_user(id):
    return User.query.get(str(id))
