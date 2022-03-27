"""
Tweet Service

Uses Twitter API. For more information, see:

https://developer.twitter.com/
"""
from functools import cached_property
import tweepy
import random
from math import ceil

from config.secrets import TWITTER


#
# Constants
#
BASE_SERVICE_URL = 'https://pinboard.in'


#
# Module Methods
#


#
# Service Class
#
class TweetService:
    #
    # Properties
    #
    @cached_property
    def favorites(self):
        faves = []
        pages = 0

        cursor_params = {
            'id': self.user,
            'wait_on_rate_limit': self.wait_on_rate_limit,
            'tweet_mode': self.tweet_mode,
            'count': self.count_per_page
        }

        # https://stackoverflow.com/q/39840571/1093087
        for page in tweepy.Cursor(self.api.get_favorites, **cursor_params).pages(self.max_page):
            pages += 1
            for fave in page:
                faves.append(fave)

        return faves

    #
    # Instance Methods
    #
    def __init__(self):
        auth = tweepy.OAuth2BearerHandler(TWITTER['bearer-token'])
        self.api = tweepy.API(auth)
        self.user = TWITTER['user']

        self.tweet_mode = 'extended'
        self.wait_on_rate_limit = 'wait_on_rate_limit'
        self.count_per_page = 200
        self.max_page = 100
