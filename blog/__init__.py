from flask import Flask

def create_app():
    # More on DB init here...
    ''' Create Flask app '''
    app = Flask(__name__)

    with app.app_context():
        # Module imports
        from blog.api import api_controller
        from blog.about import about_controller
        from blog.contact import contact_controller
        from blog.posts import posts_controller

        # Register blueprints
        app.register_blueprint(api_controller.api_bp)
        app.register_blueprint(about_controller.about_bp)
        app.register_blueprint(contact_controller.contact_bp)
        app.register_blueprint(posts_controller.posts_bp, url_prefix="/blog")

    return app