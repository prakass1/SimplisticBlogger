from flask import Flask

def create_admin_app():
    # More on DB init here...
    ''' Create Flask app '''
    app = Flask(__name__)

    with app.app_context():
        # Module imports
        from .api import api_controller 
        from .auth import auth_controller

        # Register blueprints
        app.register_blueprint(api_controller.api_bp)
        app.register_blueprint(auth_controller.auth_bp, url_prefix="/admin")

    return app