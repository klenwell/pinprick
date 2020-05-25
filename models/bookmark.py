"""
Bookmark Model

This is based on Pinboard service.
"""
from urllib.parse import urlparse

from config.services import PINBOARD_BASE_URL
from config.secrets import PINBOARD_USER


class Bookmark:
    def __init__(self, attrs=None):
        if not attrs:
            attrs = {}

        self.url = attrs.get('url')
        self.title = attrs.get('title')
        self.description = attrs.get('description')
        self.service_url = attrs.get('service_url')
        self.service = attrs.get('service')
        self.created_at = attrs.get('created_at')
        self.tags = attrs.get('tags', [])

    @property
    def domain(self):
        if not self.url:
            return None

        return urlparse(self.url).netloc

    @staticmethod
    def create_from_pinboard(pinboard, indexed_tags=None):
        bookmark = Bookmark()
        bookmark.service = pinboard
        bookmark.url = pinboard.url
        bookmark.title = pinboard.description
        bookmark.description = pinboard.extended
        bookmark.created_at = pinboard.time

        if indexed_tags:
            for tag_name in pinboard.tags:
                self.tags.append(indexed_tags[tag_name])

        bookmark.service_url = bookmark.generate_pinboard_service_url()
        return bookmark

    #
    # Instance Methods
    #
    def generate_pinboard_service_url(self):
        """Pinboard does not provide a URL or unique ID that can be used to generate a URL
        even though they exist. For example: https://pinboard.in/u:tatwell/b:bd5e02362ae6

        So instead, we use the least frequent bookmark tag to generate a URL.
        """
        tag_format = '{}/u:{}/t:{}'

        if not self.tags:
            return None

        sorted_tags = sorted(self.tags, key=lambda t: t.count)
        least_used_tag = sorted_tags[0]
        return tag_format.format(PINBOARD_BASE_URL, PINBOARD_USER, least_used_tag.name)

    def __repr__(self):
        formatting = '<Bookmark title="{}" domain="{}" service_url="{}">'
        return formatting.format(self.title, self.domain, self.service_url)
