"""
Bookmark Model

This is based on Pinboard service.
"""
from urllib.parse import urlparse


class Bookmark:
    def __init__(self, **attrs):
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

    @property
    def created_on(self):
        return self.created_at.date()

    @staticmethod
    def create_from_pinboard_post(post, service):
        bookmark = Bookmark()
        bookmark.service = service
        bookmark.url = post.url
        bookmark.title = post.description
        bookmark.description = post.extended
        bookmark.created_at = post.time
        bookmark.tags = bookmark.collect_pinboard_tags(post.tags, service)
        bookmark.service_url = bookmark.generate_pinboard_service_url(service)
        return bookmark

    #
    # Instance Methods
    #
    def collect_pinboard_tags(self, tag_names, service):
        pinboard_tags = []

        if not service.tags_indexed_by_name:
            return []

        for tag_name in tag_names:
            pinboard_tag = service.tags_indexed_by_name[tag_name]
            pinboard_tags.append(pinboard_tag)

        return pinboard_tags

    def generate_pinboard_service_url(self, service):
        """Pinboard does not provide a URL or unique ID that can be used to generate a URL
        even though they exist. For example: https://pinboard.in/u:klenwell/b:bd5e02362ae6

        So instead, we use the tags to generate a URL like:
        https://pinboard.in/u:klenwell/t:some_tag/t:another_tag
        """
        service_url = '{}/u:{}'.format(service.base_url, service.user)

        for tag in self.tags:
            service_url = '{}/t:{}'.format(service_url, tag.name)

        return service_url

    def tag_to_url(self, tag):
        tag_url_f = '{}/u:{}/t:{}'
        return tag_url_f.format(self.service.base_url, self.service.user, tag.name)

    def is_created_this_day(self, month, day):
        return self.created_on.month == month and self.created_on.day == day

    def __repr__(self):
        formatting = '<Bookmark title="{}" domain="{}" service_url="{}">'
        return formatting.format(self.title, self.domain, self.service_url)
