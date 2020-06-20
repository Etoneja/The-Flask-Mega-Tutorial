from flask import Flask
from flask_migrate import Migrate

from config import Config
from app.models import User, Post
from app.database import db
from app.routes import blog
from app.auth import login


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(blog, url_prefix='')
