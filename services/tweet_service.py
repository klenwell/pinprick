"""
Tweet Service

Uses Twitter API. For more information, see:

https://developer.twitter.com/
"""
from functools import cached_property
import tweepy
import random

from config.secrets import TWITTER
from services.bookmark_service import shard_list


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
            'screen_name': self.user,
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
        self.count_per_page = 200
        self.max_page = 100

    def faves_by_date(self, dated):
        faves = []
        for fave in self.favorites:
            if fave.created_at.month == dated.month and fave.created_at.day == dated.day:
                faves.append(fave)
        return faves

    def faves_sharded_sample(self, count):
        """For given count, will break faves into groups evenly divided by and
        return one random fave from each group.
        """
        sharded_faves = []

        faves = sorted(self.favorites, key=lambda f: f.created_at)
        fave_pools = shard_list(faves, count)

        for fave_pool in fave_pools:
            fave = random.choice(fave_pool)
            sharded_faves.append(fave)

        return sharded_faves
