from os import environ
import datetime
import pytest
from flask import url_for
from common.models import posts_model
from dotenv import load_dotenv, find_dotenv
from blog import create_app
from blog.posts.service import posts_blog_service


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv(find_dotenv())

@pytest.fixture(scope="module")
def test_client():
    app_config = environ.get("APP_CONFIG")
    test_app = create_app(app_config)
    with test_app.test_client() as testing_client:
        yield testing_client

@pytest.fixture(scope="module")
def test_context():
    app_config = environ.get("APP_CONFIG")
    test_app = create_app(app_config)
    with test_app.app_context() as testing_context:
        yield testing_context

def test_serialize(test_client):
    post_db_obj = posts_model.Posts(content="test content",
            posted_date = datetime.datetime.now(),
            title = "test title",
            author = "test author"
            )
    serialized_obj = posts_blog_service.serialize(post_db_obj)
    test_stub = {
        "content": "test content",
        "posted_date": datetime.datetime.now().strftime('%B %d, %Y'),
        "title": "test title",
        "author": "test author"
    }

    assert test_stub == serialized_obj

def test_get_posts_html_resp(test_context):
    test_stub_items = list()
    test_stub = {
        "content": "test content",
        "posted_date": datetime.datetime.now().strftime('%B %d, %Y'),
        "title": "test title",
        "author": "test author"
    }
    test_stub_items.append(test_stub)
    print(test_stub)
    test_html_str = "<a href=" + "/post/" + test_stub_items[0]["title"] + ">" + "<h2 class='post-title'>" + test_stub_items[0]["title"] + \
            "</h2></a>" + "<p class='post-meta'>Posted by " + "<a href='#'>" + \
            test_stub_items[0]["author"] + "</a> on " + test_stub_items[0]["posted_date"] + "</p></div><hr>"
    html_resp = posts_blog_service.get_posts_html_resp(test_stub_items, 10, None)
    print(test_html_str)
    print(html_resp)

    assert test_html_str == html_resp

