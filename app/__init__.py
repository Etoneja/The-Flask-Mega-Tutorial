from flask import Flask
from flask_migrate import Migrate

from config import Config
from app.logger import create_logger

app = Flask(__name__)
app.config.from_object(Config)
create_logger(app)

from app.models import User, Post
from app.database import db
from app.routes import blog
from app.auth import login
from app.errors import error_404, error_500

db.init_app(app)
login.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(blog, url_prefix='')
