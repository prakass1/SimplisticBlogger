from flask import url_for
from blog import cache


def serialize(obj):
    return {
        "content": obj.content,
        "posted_date": obj.posted_date.strftime('%B %d, %Y'),
        "title": obj.title,
        "author": obj.author
    }

def get_posts_html_resp(serialized_obj, post_len, new_limit):
    str_concat = ""
    for post_obj in serialized_obj:
        if cache.get(str(post_len)):
            str_concat = cache.get(str(post_len))
        else:
            str_concat += "<a href=" + url_for('posts.get_post_title', blog_title=post_obj["title"]) + ">" + "<h2 class='post-title'>" + post_obj["title"] + \
            "</h2></a>" + "<p class='post-meta'>Posted by " + "<a href='#'>" + \
            post_obj["author"] + "</a> on " + post_obj["posted_date"] + "</p></div><hr>"
    cache.set(str(post_len), str_concat, timeout=50)
    return str_concat
    #if post_len > limit:
    #    # Add load more content
    #    str_concat += "<div class='clearfix'>" + "<button class='btn btn-primary float-right' id='load_more'>Older Posts &rarr;</button>" + \
    #        "<input type='hidden' name='prev_limit' id='prev_limit' value=" + "'" + str(limit) + "'" + "/>"
    #return str_concat
