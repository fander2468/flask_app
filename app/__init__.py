from flask import Flask
from config import Config
# Import flask wrappers
from flask_login import LoginManager # for logging users in and maintaining a sesion
from flask_sqlalchemy import SQLAlchemy # This is used to talk to our database
from flask_migrate import Migrate # Makes altering the Database a lot easier

app = Flask(__name__)
app.config.from_object(Config)

# init Login Manager
login = LoginManager(app) # used to login users and create a session
login.login_view = 'login' # Used to redirect users if they enter wrong credentials or they are an invalid user

# init the database from_object
db = SQLAlchemy(app) # create a variable to talk to db and pass in the flask app 

# init Migrate
migrate = Migrate(app, db)

from app import routes