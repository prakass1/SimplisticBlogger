from flask import Flask
from common import db, cache
from os import environ
from dotenv import load_dotenv, find_dotenv
from instance.config import app_config

load_dotenv(find_dotenv())

blog_header = environ.get("blog_header")
blog_subheader = environ.get("blog_subheader")
social_git = "#" if environ.get(
    "social_git") == "" else environ.get("social_git")
social_linkedin = "#" if environ.get(
    "social_linkedin") == "" else environ.get("social_linkedin")
social_stack = "#" if environ.get(
    "social_stack") == "" else environ.get("social_stack")

resp = resp = {"blog_header": blog_header, "blog_subheader": blog_subheader,
            "social_git": social_git, "social_linkedin": social_linkedin, "social_stack": social_stack}


def create_app(config_name):
    # More on DB init here...
    ''' Create Flask app '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # init sql-alchemy
    db.init_app(app)
    # init cache to app
    cache.init_app(app)
    
    with app.app_context():
        # Module imports
        from blog.api import api_controller
        from blog.about import about_controller
        from blog.contact import contact_controller
        from blog.posts import posts_controller
        from common.controller import posts_api_controller
        from common.controller import images_api_controller

        # Clear cache
        cache.clear()

        # Register blueprints
        app.register_blueprint(api_controller.api_bp)
        app.register_blueprint(about_controller.about_bp)
        app.register_blueprint(contact_controller.contact_bp)
        app.register_blueprint(posts_controller.posts_bp, url_prefix="/blog")
        app.register_blueprint(posts_api_controller.posts_api_bp)
        app.register_blueprint(images_api_controller.image_bp)

    return app