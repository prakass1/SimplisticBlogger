from flask import Flask
from os import environ
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv, find_dotenv
from instance.config import app_config
from flask_login import LoginManager
from common import  db, cache
from flask_wtf.csrf import CSRFProtect
from common import mail

login_manager = LoginManager()
csrf_protect = CSRFProtect()

username = environ.get("ADMIN_USERNAME")
password = environ.get("PASSWORD")
f_name = environ.get("F_NAME")
email = environ.get("EMAIL")

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
    # init csrf
    csrf_protect.init_app(app)
    # init cache
    cache.init_app(app)
    # init email
    mail.init_app(app)

    # Set the login manager
    login_manager.login_view = 'auth.admin'
    login_manager.init_app(app)

    with app.app_context():
        from common.services.users_service import UserService
        
        db.create_all()

        

        #Query table to check if admin is already present then simply do not create a user...

        # Create the admin user as per configs
        user_obj = UserService()
        admin = user_obj.query_single_user(user_name=username)
        if admin == -1:
            print("Creating the user for the first time")
            return_type = user_obj.create_user(username, generate_password_hash(password), f_name, email)
            if return_type == -1:
                print("There has been an error while creating the admin user. Check logs")
            else:
                print("Admin user has been created and can be logged in")
        
        from common.models import users_model
        @login_manager.user_loader
        def load_user(user_id):
            # Query by user_id of the Users table
            return users_model.Users.query.get(int(user_id))

        # Module imports
        from blog_admin.api import api_controller
        from blog_admin.auth import auth_controller
        from blog_admin.posts import posts_controller
        from blog_admin.posts import comments_controller
        from common.controller import posts_api_controller
        from common.controller import images_api_controller
        from common.controller import comments_api_controller

        # Register blueprints
        app.register_blueprint(api_controller.api_bp)
        app.register_blueprint(auth_controller.auth_bp, url_prefix="/admin")
        app.register_blueprint(posts_controller.posts_bp, url_prefix="/admin")
        app.register_blueprint(comments_controller.comments_bp, url_prefix="/admin")
        app.register_blueprint(posts_api_controller.posts_api_bp, url_prefix="/api")
        app.register_blueprint(images_api_controller.image_bp)
        app.register_blueprint(comments_api_controller.comments_bp)

    return app
