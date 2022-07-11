import json
from typing import Optional
from const import (POSTS_PATH,
                   COMMENTS_PATH)


def _load_json_file(filename: str) -> list[dict]:
    """ Загрузить JSON файл """
    with open(filename, encoding='utf8') as file:
        return json.load(file)


def _save_json_file(filename: str, data: list[dict]) -> None:
    """ Сохранить как JSON файл """
    with open(filename, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_posts_all() -> list[dict]:
    """ Загрузить посты из файла """
    return _load_json_file(POSTS_PATH)


def get_comments_all() -> list[dict]:
    """ Загрузить комментарии из файла """
    return _load_json_file(COMMENTS_PATH)


def get_posts_by_user(posts: list[dict], user_name: str) -> list[dict]:
    """ Получить посты по имени пользователя """
    is_user_exist = False
    user_posts = []
    for post in posts:
        if user_name.lower() == post["poster_name"].lower():
            is_user_exist = True
            user_posts.append(post)
    if not is_user_exist:
        raise ValueError(f'User with name "{user_name}" is not exist')
    return user_posts


def get_comments_by_post_id(comments: list[dict], post_id: int) -> list[dict]:
    """ Получить комментарии поста по его идентификатору """
    is_post_exist = False
    post_comments = []
    for comment in comments:
        if post_id == comment["post_id"]:
            is_post_exist = True
            post_comments.append(comment)
    if not is_post_exist:
        raise ValueError(f'Post with id = "{post_id}" is not exist')
    return post_comments


def search_for_posts(posts: list[dict], query: str) -> list[dict]:
    """ Получить посты содержащие query """
    query_posts = []
    if not query:
        return query_posts
    for post in posts:
        if query.lower() in post["content"].lower():
            query_posts.append(post)
    return query_posts


def get_post_by_pk(posts: list[dict], pk: int) -> Optional[dict]:
    """ Получить пост по идентификатору """
    for post in posts:
        if pk == post["pk"]:
            return post
    return None
