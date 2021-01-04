from common import db
from common.models.reply_model import Replies

class Comments(db.Model):
    __tablename__="comments"
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_uuid = db.Column(db.String(255))
    author_email = db.Column(db.String(255), nullable=False)
    author_name = db.Column(db.String(255), nullable=False)
    author_comment = db.Column(db.String(255))
    posted_date = db.Column(db.DateTime)
    comment_state = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.p_id"))
    replies = db.relationship("Replies", backref="comments", lazy="dynamic")
