import datetime
import traceback
from sqlalchemy import exc
from common import db
from common.models import posts_model
from common.models import images_model
from common.models import tags_model
from common import cache

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
    
    def delete_post(self, post, tags):
        try:
            #get the tags associated with the post
            #tags = tags_model.Tags.query.filter_by(post=post).all()
            if tags:
                for db_tag in tags:
                    db.session.delete(db_tag)
                    db.session.commit()
            db.session.delete(post)
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
    
    def edit_post(self, post, db_tags, new_title, new_content, new_image_list, new_tags_list):
        try:
            post.title = new_title
            post.content = new_content
            post.posted_date = datetime.datetime.now()
            db.session.add(post)
            db.session.commit()
            db_image_obj = images_model.Images.query.filter_by(posts=post).all()
            db_img_list = [db_image.image_url for db_image in db_image_obj]
            self.cmp_add(new_image_list, db_img_list, post, "IMAGES")
            # Add the tags
            #db_tag_obj = tags_model.Tags.query.filter_by(posts=post).all()
            db_tag_list = [db_tag.tag for db_tag in db_tags]
            if ("uncategorized" not in new_tags_list) and ("uncategorized" in db_tag_list):
                print("True")
                db_tag_list.remove("uncategorized")
                tag = tags_model.Tags.query.filter_by(tag="uncategorized", posts=post).first()
                db.session.delete(tag)
                db.session.commit()
            self.cmp_add(new_tags_list, db_tag_list, post, "TAG")
            return True
        except exc.SQLAlchemyError:
            return False

    @classmethod
    def count_post(cls):
        post_count = posts_model.Posts.query.count()
        return post_count
    
    @classmethod
    def get_all_posts(cls, order_by=False, is_admin=False):
        if is_admin and order_by:
            posts = posts_model.Posts.query.order_by(posts_model.Posts.posted_date.desc()).all()
        if is_admin:
            posts = posts_model.Posts.query.all()
        elif cache.get("all-posts-ordered"):
            print("Retreiving the posts from cache")
            posts = cache.get("all-posts-ordered")
        elif order_by:
            posts = posts_model.Posts.query.order_by(posts_model.Posts.posted_date.desc()).all()
            print("Not yet cached, caching all posts")
            cache.set("all-posts-ordered", posts, timeout=50)
        elif cache.get("all-posts"):
            print("Retreiving the posts from cache")
            posts = cache.get("all-posts")
        else:
            posts = posts_model.Posts.query.all()
            print("Not yet cached, caching all posts")
            cache.set("all-posts", posts, timeout=50)
        return posts
    
    @classmethod
    def get_post_by_title(cls, post_title, is_admin=False):
        if is_admin:
            post = posts_model.Posts.query.filter_by(title = post_title).first()
            tags = tags_model.Tags.query.filter_by(posts=post).all()
            post_set = [post, tags]
        elif cache.get(post_title):
            print("Retreiving from cache")
            post_set = cache.get(post_title)
        else:
            print("Not yet cached, caching the current post details")
            post = posts_model.Posts.query.filter_by(title = post_title).first()
            tags = tags_model.Tags.query.filter_by(posts=post).all()
            cache.set(post_title, [post, tags], timeout=50)
            post_set = [post, tags]
        return post_set
    
    
    @classmethod
    def get_tags_for_post(cls, post):
        db_tags = tags_model.Tags.query.filter_by(posts=post).all()
        tags_strings = ",".join(db_tag.tag for db_tag in db_tags)
        return tags_strings
    
    @classmethod
    def serialize_tags(cls, db_tags):
        tags_strings = ",".join(db_tag.tag for db_tag in db_tags)
        return tags_strings

