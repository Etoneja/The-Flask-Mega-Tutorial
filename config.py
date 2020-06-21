import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(BASEDIR, "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # python -m smtpd -n -c DebuggingServer localhost:8025
    # MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    # MAIL_PORT = int(os.environ.get("MAIL_PORT", 8025))
    # MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    # ADMINS = ["admin@etoneja.pw"]

    POSTS_PER_PAGE = 3
