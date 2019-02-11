from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_session import Session

from config import config_dict

db = SQLAlchemy()

def create_app(config_name):

    app=Flask(__name__)
    app.config.from_object(config_dict('config_name'))
    Session(app)
    db.init_app(app)
    return app