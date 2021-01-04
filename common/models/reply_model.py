from common import db

class Replies(db.Model):
    __tablename__="replies"
    reply_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    posted_date = db.Column(db.DateTime)
    author_email = db.Column(db.String(255), nullable=False)
    reply_state = db.Column(db.String(255), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.comment_id"))
