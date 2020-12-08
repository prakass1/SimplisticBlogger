from common import db
from common.models.images_model import Images

class Posts(db.Model):
    __tablename__ = "posts"
    p_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    posted_date = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)
    images = db.relationship("Images", backref="posts", lazy=True)
