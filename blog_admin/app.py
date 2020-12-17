from blog_admin import create_admin_app
from os import environ

config_name = environ.get("APP_CONFIG")
admin_app = create_admin_app(config_name)


if __name__ == '__main__':
    admin_app.run(host=str(environ.get("FLASK_HOST")), port=str(environ.get("FLASK_ADMIN_PORT")))
