import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt = JWTManager(app)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        
        from .api import items
        from .views import auth
        app.register_blueprint(items.items_bp)
        app.register_blueprint(auth.auth_bp)

        # create database if it doesn't exist
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()

    return app