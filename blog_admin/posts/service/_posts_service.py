import datetime
import traceback
from sqlalchemy import exc
from common import db
from common.models import posts_model
from common.models import images_model
from common.models import tags_model

class PostService(object):
    def __init__(self):
        pass

    def add_post(self, blog_title, blog_author, blog_content, curr_user, image_list, post_tags_list):
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
            # Add the tags
            model_tags_list = [tags_model.Tags(tag=tag, posts=posts) for tag in post_tags_list]
            db.session.add_all(model_tags_list)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            traceback.print_exc()
            return False

    
    def view_post(self):
        pass
    
    def delete_post(self, post):
        try:
            #get the tags associated with the post
            tags = tags_model.Tags.query.filter_by(post=post).all()
            if tags:
                db.session.delete(tags)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            traceback.print_exc()
            return False
    
    def cmp_add(self,new_items, db_items, reference, db_type):
        for item in new_items:
            if item not in db_items:
                if db_type == "IMAGES":
                    db_obj = images_model.Images(image_url = item, posts=reference)
                elif db_type=="TAG":
                    db_obj = tags_model.Tags(tag = item, posts=reference)
                db.session.add(db_obj)
                db.session.commit()
    
    def edit_post(self, post, new_title, new_content, new_image_list, new_tags_list):
        try:
            post.title = new_title
            post.content = new_content
            db.session.add(post)
            db.session.commit()
            db_image_obj = images_model.Images.query.filter_by(posts=post).all()
            db_img_list = [db_image.image_url for db_image in db_image_obj]
            self.cmp_add(new_image_list, db_img_list, post, "IMAGES")
            # Add the tags
            db_tag_obj = tags_model.Tags.query.filter_by(posts=post).all()
            db_tag_list = [db_tag.tag for db_tag in db_tag_obj]
            self.cmp_add(new_tags_list, db_tag_list, post, "TAG")
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
