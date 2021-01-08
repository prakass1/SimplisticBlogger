import datetime
import traceback
import uuid
import os
from libgravatar import Gravatar
from sqlalchemy import exc, and_
from common import db, cache
from common.models import posts_model, comments_model
from common.services.comment_state_enums import States
from common.services.utility import send_email, check_reply


class CommentService():
    def __init__(self):
        pass

    @classmethod
    def serialize_comments(cls, comments_db_obj, is_admin=False):
        comments_list = list()
        for comment_db_obj in comments_db_obj:
            if is_admin:
                comments_list.append({
                    "author_name": comment_db_obj.author_name,
                    "author_email": comment_db_obj.author_email,
                    "comment_ref_id": comment_db_obj.comment_uuid,
                    "content": comment_db_obj.author_comment,
                    "posted_date": comment_db_obj.posted_date.strftime('%B %d, %Y'),
                    "post_link": "http://" + os.environ.get("FLASK_HOST") + ":" + os.environ.get("FLASK_BLOG_PORT") + "/blog/" + comment_db_obj.posts.title
                })
            else:
                comments_list.append({
                    "author_name": comment_db_obj.author_name,
                    "author_email": comment_db_obj.author_email,
                    "comment_ref_id": comment_db_obj.comment_uuid,
                    "content": comment_db_obj.author_comment,
                    "image_url": Gravatar(comment_db_obj.author_email).get_image(default="robohash"),
                    "posted_date": comment_db_obj.posted_date.strftime('%B %d, %Y'),
                })

        return comments_list

    def add_comment(self, author_name, author_email, author_comment, post_db_obj, is_admin=False):
        try:
            if is_admin:
                comment_state = States.APPROVED.value
            else:
                comment_state = States.UNDER_MODERATION.value

            comment_db_obj = comments_model.Comments(author_name=author_name,
                                                     author_email=author_email,
                                                     author_comment=author_comment,
                                                     comment_uuid=str(
                                                         uuid.uuid4()).split("-")[0],
                                                     posted_date=datetime.datetime.now(),
                                                     comment_state= comment_state,
                                                     posts=post_db_obj)
            db.session.add(comment_db_obj)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            traceback.print_exc()
            return False

    @classmethod
    def send_email(cls, author_comment, author_name, post_db_obj):
        c_name_tuple, c_status = check_reply(author_comment, post_db_obj)
        if c_name_tuple and c_status:
            e_status = send_email(author_comment, author_name, c_name_tuple, post_db_obj)
            if e_status:
                print("The reply email is sent to -- ", c_name_tuple[0])
                return True
            else:
                print("error while sending the email reply")
                return False
        else:
            return False
    
    @classmethod
    def get_comment_count(cls, is_admin=False):
        try:
            if is_admin:
                count = comments_model.Comments.query.filter_by(comment_state=States.UNDER_MODERATION.value).count()
            else:
                count = comments_model.Comments.query.filter_by(comment_state=States.APPROVED.value).count()
            return count
        except exc.SQLAlchemyError:
            traceback.print_exc()
            return 0

    @classmethod
    def get_comments(cls, post_db_obj=None, is_admin=False):
        if not post_db_obj and is_admin:
            comments = comments_model.Comments.query.filter_by(
                comment_state=States.UNDER_MODERATION.value).all()
        elif post_db_obj and is_admin:
            comments = comments_model.Comments.query.filter_by(posts=post_db_obj).filter_by(
                comment_state=States.UNDER_MODERATION.value).all()
        elif post_db_obj and not is_admin:
            comments = comments_model.Comments.query.filter_by(posts=post_db_obj).filter_by(
                comment_state=States.APPROVED.value).all()

        serialized_comments = cls.serialize_comments(comments, is_admin)
        return serialized_comments

    def get_comment(self):
        pass

    def delete_comment(self):
        pass

    def edit_comment(self, comment_ref_id, comment_status):
        try:
            #If the status is reject delete from db
            comment = comments_model.Comments.query.filter_by(comment_uuid=comment_ref_id).first()
            if comment:
                if int(comment_status) == States.REJECTED.value:
                    db.session.delete(comment)
                    db.session.commit()
                    return {"resp":True, "message": "Deleted Comment"}
                elif int(comment_status) == States.APPROVED.value:
                    # Edit the comment to be accept for posting
                    comment.comment_state = States.APPROVED.value
                    db.session.add(comment)
                    db.session.commit()
                    return {"resp":True, "message": "Approved Comment"}
            else:
                return {"resp":False, "message": "Comment does not exist in DB"}
        except (exc.SQLAlchemyError, AttributeError):
            traceback.print_exc()
            return {"resp": False, "message":"Internal System Error has occurred"}