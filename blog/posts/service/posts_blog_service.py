from flask import url_for
from blog import cache


def serialize(obj):
    return {
        "content": obj.content,
        "posted_date": obj.posted_date.strftime('%B %d, %Y'),
        "title": obj.title,
        "author": obj.author
    }

@cache.cached(timeout=50, key_prefix="more_posts")
def get_posts_html_resp(serialized_obj, post_len, limit):
    str_concat = ""
    for post_obj in serialized_obj:
        str_concat += "<a href=" + url_for('posts.get_post_title', blog_title=post_obj["title"]) + ">" + "<h2 class='post-title'>" + post_obj["title"] + \
            "</h2></a>" + "<p class='post-meta'>Posted by " + "<a href='#'>" + \
            post_obj["author"] + "</a> on " + post_obj["posted_date"] + "</p></div><hr>"
    if post_len > limit:
        # Add load more content
        str_concat += "<div class='clearfix'>" + "<button class='btn btn-primary float-right' id='load_more'>Older Posts &rarr;</button>" + \
            "<input type='hidden' name='prev_limit' id='prev_limit' value=" + str(limit) + "/>"
    return str_concat