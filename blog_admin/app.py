from blog_admin import create_admin_app
from blog_admin import login_manager
from os import environ

config_name = environ.get("APP_CONFIG")
admin_app = create_admin_app(config_name)

from blog_admin.auth.model.users_model import Users

@login_manager.user_loader
def load_user(user_id):
    # Query by user_id of the Users table
    return Users.query.get(int(user_id))
        

if __name__ == '__main__':
    admin_app.run(host="0.0.0.0", port=9001)
