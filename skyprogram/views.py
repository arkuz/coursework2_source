import logging
import const
import utils
from flask import Blueprint, render_template, request, jsonify

logger = logging.getLogger(__name__)
skyprogram_blueprint = Blueprint('skyprogram_blueprint', __name__, template_folder='templates')


@skyprogram_blueprint.route('/')
def index_page():
    posts = utils.get_posts_all()
    return render_template('index.html', posts=posts)


@skyprogram_blueprint.route('/post/<int:pk>/')
def post_page(pk):
    post = utils.get_post_by_pk(utils.get_posts_all(), pk)
    try:
        comments = utils.get_comments_by_post_id(utils.get_comments_all(), pk)
    except ValueError as e:
        logger.error(e)
        title = const.ERROR_500['code']
        return render_template('error_page.html', title=title, text=e), const.ERROR_500['text']
    return render_template('post.html', post=post, comments=comments)


@skyprogram_blueprint.route('/search/')
def search_page():
    query = request.args.get('s', '')
    posts = utils.search_for_posts(utils.get_posts_all(), query)
    limit = 10
    if len(posts) > limit:
        posts = posts[:limit]
    logger.info(f'Выполнен поиск по фразе "{query}"')
    return render_template('search.html', posts=posts, query=query)


@skyprogram_blueprint.route('/users/<username>/')
def user_page(username):
    try:
        posts = utils.get_posts_by_user(utils.get_posts_all(), username)
    except ValueError as e:
        logger.error(e)
        title = const.ERROR_500['code']
        return render_template('error_page.html', title=title, text=e), const.ERROR_500['text']
    return render_template('user-feed.html', posts=posts)


@skyprogram_blueprint.errorhandler(const.ERROR_404['code'])
def error_page_404(e):
    title = const.ERROR_404['code']
    text = const.ERROR_404['text']
    return render_template('error_page.html', title=title, text=text), const.ERROR_404['code']


@skyprogram_blueprint.errorhandler(const.ERROR_500['code'])
def error_page_500(e):
    title = const.ERROR_500['code']
    text = const.ERROR_500['text']
    return render_template('error_page.html', title=title, text=text), const.ERROR_500['text']


@skyprogram_blueprint.route('/api/posts/')
def api_posts():
    posts = utils.get_posts_all()
    return jsonify(posts)


@skyprogram_blueprint.route('/api/post/<int:pk>/')
def api_post(pk):
    post = utils.get_post_by_pk(utils.get_posts_all(), pk)
    try:
        comments = utils.get_comments_by_post_id(utils.get_comments_all(), pk)
    except ValueError as e:
        logger.error(e)
        return jsonify({'type': 'error',
                        'code': const.ERROR_500['code'],
                        'message': str(e)})
    return jsonify({'post': post,
                    'comments': comments})
