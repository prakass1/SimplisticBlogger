from blog import create_app
from os import environ

config_name = environ.get("APP_CONFIG")
app = create_app(config_name)

if __name__ == '__main__':
    app.run(port=str(environ.get("FLASK_ADMIN_PORT")), host="0.0.0.0")
