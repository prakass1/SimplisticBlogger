from common import db
from common.models.images_model import Images
from common.models.tags_model import Tags
from common.models.comments_model import Comments

class Posts(db.Model):
    __tablename__ = "posts"
    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    posted_date = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    modified_flag = db.Column(db.Boolean, default=False)
    images = db.relationship("Images", backref="posts", lazy=True)
    category = db.relationship("Tags", backref="posts", lazy="dynamic")
    comments = db.relationship("Comments", backref="posts", lazy="dynamic")
