"""
Collect favorites from Twitter account.

USAGE:
    python tweets.py usage
"""
import sys
import random
from datetime import datetime, timedelta, timezone

from services.tweet_service import TweetService
from models.timeline import Timeline
from mailers.daily_tweet_mailer import DailyTweetMailer
from mailers.timeline_mailer import TimelineMailer


#
# Actions
#
def usage():
    USAGE = """
USAGE

To experiment with command line:
    python tweets.py interactive

To send email:
    python tweets.py favorites <user>@example.com
"""
    print(USAGE)


# Usage: python tweets.py daily_mailer <user>@example.com
def daily_mailer(args):
    recipient = args[1]
    mailer = DailyTweetMailer()
    mailer.deliver_to(recipient)
    print('Daily tweet mailer delivered to {}'.format(recipient))
    return True


# Usage: python main.py timeline <hours_ago> <email>
def timeline(args):
    hours = int(args[1])
    recipient = args[2]
    minutes = hours * 60
    start_at = datetime.now(timezone.utc) - timedelta(minutes=minutes)

    timeline = Timeline()
    tweets = timeline.fetch_since(start_at)

    mailer = TimelineMailer(tweets)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))
    return True


# Usage: python tweets.py interactive
def interactive():
    test_bearer_token()


def test_bearer_token():
    api = TweetService()
    faves = api.favorites

    indexed = {}
    for fave in faves:
        key = (fave.created_at.month, fave.created_at.day)
        if indexed.get(key):
            indexed[key].append(fave)
        else:
            indexed[key] = [fave]

    date_count = [(d, len(indexed[d])) for d in indexed.keys()]
    print(len(faves), sorted(date_count))

    tweet = faves[random.randint(0, len(faves)-1)]
    print(tweet._json)
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
    elif command == 'timeline':
        timeline(args)
    else:
        usage()


#
# Main
#
if __name__ == '__main__':
    controller()
