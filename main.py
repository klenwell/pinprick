"""
Email random bookmarks from a Pinboard Account.

USAGE:
    python main.py usage
"""
import sys
import random
from datetime import datetime, timedelta, timezone
import tweepy

from services.bookmark_service import BookmarkService
from services.tweet_service import TweetService
from mailers.daily_mailer import DailyMailer
from mailers.gmail_smtp_mailer import GmailSmtpMailer
from config.secrets import TIMELINE


#
# Actions
#
def usage():
    USAGE = """
USAGE

To experiment with command line:
    python main.py interactive

To send email:
    python main.py daily_mailer <user>@example.com
"""
    print(USAGE)


# Usage: python main.py daily_mailer <email>
def daily_mailer(args):
    recipient = args[1]

    mailer = DailyMailer()
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))
    return "Done"


# Usage: python main.py music_mailer <email>
def music_mailer(args):
    tags = ['music', 'youtube']
    num_bookmarks = 3
    subject = 'Pinprick Music Mailer'
    recipient = args[1]

    bookmarks = BookmarkService.import_by_tags(tags)
    random_bookmarks = random.sample(bookmarks, num_bookmarks)

    mailer = GmailSmtpMailer(random_bookmarks, subject=subject)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))


# Usage: python main.py timeline <hours_ago> <email>
def timeline(args):
    hours = args[1]
    recipient = args[2]
    start_at = datetime.now(timezone.utc) - timedelta(hours=hours)

    timeline = Timeline()
    tweets = timeline.fetch_since(start_at)

    mailer = TimelineMailer(tweets)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))
    return "Done"


# Usage: python main.py interactive
def interactive():
    consumer_key = TIMELINE['staging-key']
    consumer_secret = TIMELINE['staging-key-secret']
    access_token = TIMELINE['staging-access-token']
    access_token_secret = TIMELINE['staging-access-token-secret']

    # API v1
    # https://docs.tweepy.org/en/stable/examples.html
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)

    # If the authentication was successful, this should print the
    # screen name / username of the account
    print(api.verify_credentials().screen_name)
    tweets = api.home_timeline()
    breakpoint()

    # API v2
    # https://docs.tweepy.org/en/stable/examples.html
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    tweet_fields = ['id', 'author_id', 'text', 'created_at', 'context_annotations']
    expansions = ['author_id']

    # Notice timezone
    start_time = datetime.now(timezone.utc) - timedelta(hours=1)

    all_tweets = []
    all_users = []

    for response in tweepy.Paginator(
        client.get_home_timeline,
        max_results=100,
        tweet_fields=tweet_fields,
        expansions=expansions,
        start_time=start_time,
        limit=3
    ):
        tweets = response.data
        users = response.includes['users']
        print('twitter request', len(tweets), len(users))

        all_tweets += tweets
        all_users += users

    print(len(all_tweets))
    print(len(all_users))
    breakpoint()


#
# Controller
#
def controller():
    args = sys.argv[1:]
    command = args[0] if args else None

    print('Command: %s / Arguments: %s' % (command, args))

    if command == 'interactive':
        interactive()
    elif command == 'daily_mailer':
        daily_mailer(args)
    elif command == 'music_mailer':
        music_mailer(args)
    elif command == 'timeline':
        timeline(args)
    else:
        usage()


#
# Main
#
if __name__ == '__main__':
    controller()
