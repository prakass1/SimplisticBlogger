from blog_admin import db
from flask_login import UserMixin
from blog_admin import login_manager


@login_manager.user_loader
def load_user(user_id):
    # Query by user_id of the Users table
    return Users.query.get(int(user_id))

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    changed_pass = db.Column(db.Boolean(), nullable=False, default=False)
    f_name = db.Column(db.String(255), nullable=False)
    l_name = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return "<User %r>" % self.user_name
