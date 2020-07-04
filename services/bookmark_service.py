"""
Bookmark Service

Uses Pinboard API. For more information, see:

https://pinboard.in/api/
"""
from functools import cached_property
import pinboard
import random
from math import ceil

from config.secrets import PINBOARD_API_TOKEN
from models.bookmark import Bookmark


#
# Constants
#
BASE_SERVICE_URL = 'https://pinboard.in'


#
# Module Methods
#
def distributed_sample(count):
    """For given count, will break bookmarks into groups evenly divided by and
    return one random bookmark from each group.
    """
    selected_bookmarks = []

    pinboard = BookmarkService()
    bookmarks = sorted(pinboard.bookmarks, key=lambda b: b.created_at)
    bookmark_pools = shard_list(bookmarks, count)

    for bookmark_pool in bookmark_pools:
        bookmark = random.choice(bookmark_pool)
        selected_bookmarks.append(bookmark)

    return selected_bookmarks


def by_created_on_day(month, day):
    bookmarks = []

    pinboard = BookmarkService()

    for bookmark in pinboard.bookmarks:
        if bookmark.is_created_this_day(month, day):
            bookmarks.append(bookmark)

    return bookmarks


def shard_list(seq, num_shards):
    """"""
    avg_shard_size = ceil(len(seq) / num_shards)

    # Yield successive n-sized chunks from lst.
    # https://stackoverflow.com/a/312464/1093087
    for i in range(0, len(seq), avg_shard_size):
        yield seq[i:i + avg_shard_size]


#
# Service Class
#
class BookmarkService:

    def __init__(self):
        self.api = pinboard.Pinboard(PINBOARD_API_TOKEN)
        self.user = PINBOARD_API_TOKEN.split(':')[0]
        self.base_url = BASE_SERVICE_URL

    #
    # Static Methods
    #
    @staticmethod
    def import_all():
        service = BookmarkService()
        return service.bookmarks

    @staticmethod
    def import_by_tags(tags):
        bookmarks = []

        service = BookmarkService()
        posts = service.import_posts_by_tags(tags)

        for post in posts:
            bookmark = Bookmark.create_from_pinboard_post(post, service)
            bookmarks.append(bookmark)

        return bookmarks

    #
    # Properties
    #
    @cached_property
    def posts(self):
        return self.api.posts.all()

    @cached_property
    def tags(self):
        return self.api.tags.get()

    @cached_property
    def bookmarks(self):
        bookmarks = []

        service = BookmarkService()

        for post in self.posts:
            bookmark = Bookmark.create_from_pinboard_post(post, service)
            bookmarks.append(bookmark)

        return bookmarks

    @cached_property
    def tags_indexed_by_name(self):
        index = {}
        for tag in self.tags:
            index[tag.name] = tag
        return index

    #
    # Instance Methods
    #
    def import_all_posts(self):
        return self.api.posts.all()

    def import_posts_by_tags(self, tags):
        return self.api.posts.all(tag=tags)
