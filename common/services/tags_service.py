from common import cache
from common.models import tags_model, posts_model


def get_post_tags(tag_name):
    if cache.get(tag_name):
        print("Retreiving the posts from cache for the tag", tag_name)
        posts = cache.get(tag_name)
    else:
        print("Not yet cached retreiving from db for the tag", tag_name)
        tags_db_list = tags_model.Tags.query.filter_by(tag=tag_name).all()
        if len(tags_db_list) > 0:
            posts = []
            for db_tag in tags_db_list:
                print(db_tag.posts.title)
                print(db_tag.posts.posted_date)
                posts.append(db_tag.posts)
            cache.set(tag_name, posts, timeout=50)
        else:
            return False

    return posts
