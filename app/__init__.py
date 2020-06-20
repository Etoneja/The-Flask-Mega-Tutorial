from flask import Flask
from config import Config
from flask_migrate import Migrate
from app.database import db
from app.routes import blog
from app.models import User, Post


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(blog, url_prefix='')
