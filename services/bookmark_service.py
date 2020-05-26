"""
Bookmark Service

Uses Pinboard API. For more information, see:

https://pinboard.in/api/
"""
from functools import cached_property
import pinboard

from config.secrets import PINBOARD_API_TOKEN
from models.bookmark import Bookmark


BASE_SERVICE_URL = 'https://pinboard.in'


class BookmarkService:

    def __init__(self):
        self.api = pinboard.Pinboard(PINBOARD_API_TOKEN)
        self.user = PINBOARD_API_TOKEN.split(':')[0]
        self.base_url = BASE_SERVICE_URL

    @cached_property
    def tags(self):
        return self.api.tags.get()

    @cached_property
    def tags_indexed_by_name(self):
        index = {}
        for tag in self.tags:
            index[tag.name] = tag
        return index

    @staticmethod
    def import_all():
        bookmarks = []

        service = BookmarkService()
        posts = service.import_all_posts()

        for post in posts:
            bookmark = Bookmark.create_from_pinboard_post(post, service)
            bookmarks.append(bookmark)

        return bookmarks

    #
    # Instance Methods
    #
    def import_all_posts(self):
        return self.api.posts.all()

    def import_selected_posts(self):
        pass
