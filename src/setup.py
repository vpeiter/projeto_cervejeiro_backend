from flask import Flask
from flask_cors import CORS

from models import db
from config import DATABASE_URI


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app
