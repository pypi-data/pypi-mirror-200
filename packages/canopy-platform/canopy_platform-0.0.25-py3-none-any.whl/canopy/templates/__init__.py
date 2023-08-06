import collections
import pprint

import pendulum
# TODO from micropub.readability import Readability
import web
import webint_posts
from mf.util import discover_post_type
from webagt import Document
from webint_live import app

__all__ = [
    "discover_post_type",
    "pformat",
    "pendulum",
    "tx",
    "post_mkdn",
    # TODO "Readability",
    "get_first",
    "get_months",
    "get_posts",
    "get_categories",
    "Document",
    "livestream",
]

tx = web.tx
livestream = app.view.stream


def pformat(obj):
    return f"<pre>{pprint.pformat(obj)}</pre>"


def post_mkdn(content):
    return web.mkdn(content)  # XXX , globals=micropub.markdown_globals)


def get_first(obj, p):
    return obj.get(p, [""])[0]


def get_months():
    months = collections.defaultdict(collections.Counter)
    for post in webint_posts.app.model.get_posts():
        published = post["published"][0]
        months[published.year][published.month] += 1
    return months


def get_posts():
    return webint_posts.app.model.get_posts()


def get_categories():
    return webint_posts.app.model.get_categories()
