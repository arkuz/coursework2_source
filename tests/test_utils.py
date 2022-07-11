import time
import pytest
import utils
from json import JSONDecodeError

TEST_DATA_PATH = "tests/test_data"
POSTS_PATH = f"{TEST_DATA_PATH}/posts.json"
COMMENTS_PATH = f"{TEST_DATA_PATH}/comments.json"
ERROR_FILE_PATH = f"{TEST_DATA_PATH}/error_file.json"


@pytest.fixture()
def load_posts() -> list[dict]:
    return utils._load_json_file(POSTS_PATH)


@pytest.fixture()
def load_comments() -> list[dict]:
    return utils._load_json_file(COMMENTS_PATH)


class TestUtils:
    def test_load_json_file_exist_file(self, load_posts):
        posts = load_posts
        assert len(posts) == 8
        keys = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]
        for post in posts:
            for key in keys:
                assert key in post.keys()

    def test_load_json_file_not_exist_file(self):
        with pytest.raises(FileNotFoundError):
            utils._load_json_file(f'{time.time()}_{POSTS_PATH}')

    def test_load_json_file_json_decode_error(self):
        with pytest.raises(JSONDecodeError):
            utils._load_json_file(ERROR_FILE_PATH)

    def test_save_json_file_positive(self):
        filename = f'test_file_{time.time()}.json'
        test_data = {'user_id': 1, 'name': 'John'}
        utils._save_json_file(filename, [test_data])
        assert test_data == utils._load_json_file(filename)[0]

    @pytest.mark.parametrize('username, post_count', [
        ('leo', 2),
        ('johnny', 2),
        ('larry', 2),
    ])
    def test_get_posts_by_user_valid_username(self, load_posts, username: str, post_count: int):
        assert len(utils.get_posts_by_user(load_posts, username)) == post_count

    def test_get_posts_by_user_value_error(self, load_posts):
        with pytest.raises(ValueError):
            utils.get_posts_by_user(load_posts, f'username_{time.time()}')

    @pytest.mark.parametrize('pk, content_part', [
        (1, 'Ага, опять еда!'),
        (2, 'Вышел погулять днем, пока все на работе.'),
        (6, 'Вот обычная лампочка,'),
    ])
    def test_get_post_by_pk_valid_pk(self, load_posts, pk: int, content_part: str):
        post = utils.get_post_by_pk(load_posts, pk)
        assert content_part in post['content']

    def test_get_post_by_pk_invalid_pk(self, load_posts):
        pk = 99999
        assert utils.get_post_by_pk(load_posts, pk) is None

    @pytest.mark.parametrize('post_id, post_count', [
        (1, 4),
        (2, 4),
        (7, 1),
    ])
    def test_get_comments_by_post_id_valid_id(self, load_comments, post_id: int, post_count: int):
        comments = utils.get_comments_by_post_id(load_comments, post_id)
        assert len(comments) == post_count

    def test_get_comments_by_post_id_invalid_id(self, load_comments):
        with pytest.raises(ValueError):
            utils.get_comments_by_post_id(load_comments, 99999)

    @pytest.mark.parametrize('query, post_count', [
        ('для', 1),
        ('а', 8),
        ('на', 8),
        (f'слово_{time.time()}', 0),
        ('', 0),
    ])
    def test_search_for_posts(self, load_posts, query: str, post_count: int):
        assert len(utils.search_for_posts(load_posts, query)) == post_count
