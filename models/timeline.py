"""
Timeline

Uses Twitter API. For more information, see:

https://developer.twitter.com/
"""
import tweepy
from config.secrets import TIMELINE


class Timeline:
    def __init__(self):
        consumer_key = TIMELINE['staging-key']
        consumer_secret = TIMELINE['staging-key-secret']
        access_token = TIMELINE['staging-access-token']
        access_token_secret = TIMELINE['staging-access-token-secret']

        # API v2
        # https://docs.tweepy.org/en/stable/examples.html
        self.client = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )

    def fetch_since(self, start_at):
        v2_tweets = []
        v2_users = []
        pages = 0

        cursor_params = {
            'tweet_fields': ['id', 'author_id', 'text', 'created_at', 'context_annotations'],
            'expansions': ['author_id'],
            'start_time': start_at,
            'max_results': 100,  # Max 100
            'limit': 10
        }

        for response in tweepy.Paginator(self.client.get_home_timeline, **cursor_params):
            pages += 1
            paged_tweets = response.data
            paged_users = response.includes.get('users')

            if paged_tweets:
                v2_tweets += paged_tweets

            if paged_users:
                v2_users += paged_users

            print(f"Fetched page {pages}")

        return self.match_users_to_tweets(v2_tweets, v2_users)

    def match_users_to_tweets(self, v2_tweets, v2_users):
        authors = {}
        for v2_user in v2_users:
            if v2_user.id not in authors:
                authors[v2_user.id] = v2_user

        timeline_tweets = []
        for v2_tweet in v2_tweets:
            author = authors.get(v2_tweet.author_id)
            timeline_tweet = TimelineTweet(v2_tweet, author)
            timeline_tweets.append(timeline_tweet)

        return timeline_tweets


class TimelineTweet:
    def __init__(self, v2_tweet, author):
        self.tweet = v2_tweet
        self.author = author

    @property
    def text(self):
        return self.tweet.text

    @property
    def url(self):
        if self.author_url:
            return f"{self.author_url}/status/{self.tweet.id}"
        else:
            # Source: https://stackoverflow.com/a/61919300/1093087
            return f"https://twitter.com/twitter/statuses/{self.tweet.id}"

    @property
    def author_url(self):
        if not self.author:
            return None
        else:
            return f"https://twitter.com/{self.author.username}"

    @property
    def created_at(self):
        return self.tweet.created_at.astimezone()

    @property
    def timestamp(self):
        return str(self.created_at)[:16]

    @property
    def by(self):
        if not self.author:
            return '?'
        else:
            return self.author.username

    def __repr__(self):
        created_at = str(self.created_at)[:16]
        blurb = self.text[:20]
        return f'<Tweet by {self.by} "{blurb}..." ({len(self.text)}) {created_at}>'
