from config import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(connexion_app.app)
