from flask import Flask
from instance.config import app_config
from flask_sqlalchemy import SQLAlchemy
from os import environ

db = SQLAlchemy()

username = environ.get("ADMIN_USERNAME")
password = environ.get("PASSWORD")
f_name = environ.get("F_NAME")

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def create_admin_app(config_name):
    ''' Create Flask app '''
    print("Initiating admin app for blogging...")
    # More on DB init here...
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # init sql-alchemy
    db.init_app(app)

    with app.app_context():
        from blog_admin.auth.service.users_service import UserService
        db.create_all()

        #Query table to check if admin is already present then simply do not create a user...

        # Create the admin user as per configs
        user_obj = UserService(username, password, f_name, l_name = "", is_active=False)
        return_type = user_obj.create_user()
        if return_type == -1:
            print("There has been an error while creating the admin user. Check logs")
        else:
            print("Admin user has been created and can be logged in")

        # Module imports
        from .api import api_controller 
        from .auth import auth_controller

        # Register blueprints
        app.register_blueprint(api_controller.api_bp)
        app.register_blueprint(auth_controller.auth_bp, url_prefix="/admin")

    return app