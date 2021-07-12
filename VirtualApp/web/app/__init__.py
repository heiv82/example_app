from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


# The 'login' value above is the function (or endpoint) name for the login view.
# In other words, the name you would use in a url_for() call to get the URL.
login.login_view = 'login'

from app import routes
from app.models import User
from app.models import Device
from app.models import DeviceData


db.create_all()
