import datetime
import traceback
from sqlalchemy import exc
from common import db
from common.models import posts_model
from common.models import images_model
import datetime

class PostService(object):
    def __init__(self):
        pass

    def add_post(self, blog_title, blog_author, blog_content, curr_user, image_list):
        try:
            posts = posts_model.Posts(content=blog_content,
            posted_date = datetime.datetime.now(),
            title = blog_title,
            author = blog_author,
            users = curr_user
            )
            db.session.add(posts)
            db.session.commit()
            model_image_list = [images_model.Images(image_url = image_url, posts=posts) for image_url in image_list]
            #print(model_image_list)
            # insert_bulk()
            db.session.add_all(model_image_list)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            traceback.print_exc()
            return False

    
    def delete_post(self, post):
        try:
            db.session.delete(post)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            traceback.print_exc()
            return False
    
    def edit_post(self, post, new_title, new_content, new_image_list):
        try:
            post.title = new_title
            post.content = new_content
            post.posted_date = datetime.datetime.now()
            db.session.add(post)
            db.session.commit()
            db_image_obj = images_model.Images.query.filter_by(posts=post).all()
            db_img_list = [db_image.image_url for db_image in db_image_obj]
            for image in new_image_list:
                if image not in db_img_list:
                    image_db_obj = images_model.Images(image_url = image, posts=post)
                    db.session.add(image_db_obj)
                    db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    @classmethod
    def count_post(cls):
        post_count = posts_model.Posts.query.count()
        return post_count
    
    @classmethod
    def get_all_posts(cls):
        posts = posts_model.Posts.query.all()
        return posts
    
    @classmethod
    def get_post_by_title(cls, post_title):
        post = posts_model.Posts.query.filter_by(title = post_title).first()
        return post
