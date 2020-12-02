from flask import Flask

def create_app():
    # More on DB init here...
    ''' Create Flask app '''
    app = Flask(__name__)

    with app.app_context():
        # Module imports
        from .about import about_controller
        from .contact import contact_controller
        from .posts import posts_controller

        # Register blueprints
        app.register_blueprint(about_controller.about_bp)
        app.register_blueprint(contact_controller.contact_bp)
        app.register_blueprint(posts_controller.posts_bp)

    return app