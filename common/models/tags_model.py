from common import db

class Tags(db.Model):
    __tablename__="tags"
    tag_id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.p_id"))
