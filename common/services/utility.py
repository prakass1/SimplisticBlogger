from os import environ
from common.models import comments_model
from flask_mail import Message
from common import mail

def check_reply(comment, post_obj):
    refer_names = list()
    words_list = comment.split(" ")
    for word in words_list:
        if len(word) >= 3 and "@" in word[0] and ":" in word[len(word) - 1]:
            refer_names.append(word.replace("@", "").replace(":",""))
    if len(refer_names) > 0:
        for name in refer_names:
            com_db_obj = comments_model.Comments.query.filter(comments_model.Comments.author_name.like("%" + name + "%"), comments_model.Comments.post_id==post_obj.p_id).first()
            if com_db_obj.author_name:
                return (com_db_obj.author_name, com_db_obj.author_email), True
    return None, False


def send_email(author_comment, author_name, c_name_tuple, post_db_obj):
    try:
        msg = Message('New message from Blog', 
        sender = environ.get("MAIL_USERNAME"),
        recipients = [c_name_tuple[1]])
        msg_body = "<h4> Hello," + c_name_tuple[0] + "There has been a reply to your comment to " + post_db_obj.title + ".</h4><br/>" 
        msg_body += "<div style='width: 30%;display: flex;flex-direction: column;border: 1px red solid;'>"
        msg_body += "<div>" + "<p>Comment: " + author_comment + "</p>" + "<p>Author: " + author_name + "</p></div>" + "</div>"
        msg.html = msg_body
        mail.send(msg)
        return True
    except (UnicodeError, TypeError, AttributeError):
        return False
