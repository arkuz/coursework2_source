import random
import pytest
from app import app


@pytest.fixture()
def client():
    return app.test_client()


class TestAPI:
    def test_api_posts(self, client):
        response = client.get('/api/posts/')
        posts = response.json
        assert type(posts) is list
        keys = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]
        for post in posts:
            for key in keys:
                assert key in post.keys()

    @pytest.mark.parametrize('pk', [
        1,
        2,
        6,
    ])
    def test_api_post_valid_pk(self, client, pk: int):
        response = client.get(f'/api/post/{pk}/')
        post = response.json
        assert type(post) is dict
        keys = ["post", "comments"]
        for key in keys:
            assert key in post

    def test_api_post_invalid_pk(self, client):
        pk = random.randint(500000, 999999)
        response = client.get(f'/api/post/{pk}/')
        post = response.json
        assert type(post) is dict
        keys = ["type", "code", "message"]
        for key in keys:
            assert key in post
