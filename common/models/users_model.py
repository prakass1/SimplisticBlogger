from common import db
from flask_login import UserMixin
from common.models.posts_model import Posts

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    changed_pass = db.Column(db.Boolean(), nullable=False, default=False)
    f_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    l_name = db.Column(db.String(255), nullable=True)
    posts = db.relationship("Posts", backref="users", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.user_name
