from flask import Flask
from instance.config import app_config

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def create_admin_app(config_name):
    print("Initiating admin app for blogging...")
    # More on DB init here...
    ''' Create Flask app '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    with app.app_context():
        # Module imports
        from .api import api_controller 
        from .auth import auth_controller

        # Register blueprints
        app.register_blueprint(api_controller.api_bp)
        app.register_blueprint(auth_controller.auth_bp, url_prefix="/admin")

    return app