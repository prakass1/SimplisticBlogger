from common import db

class Images(db.Model):
    __tablename__="images"
    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.p_id"))
