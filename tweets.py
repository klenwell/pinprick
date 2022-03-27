"""
Collect favorites from Twitter account.

USAGE:
    python main.py usage
"""
import sys
import random

from services.tweet_service import TweetService


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


# Usage: python tweets.py favorites <user>@example.com
def daily_mailer(args):
    pass


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


def test_twint():
    import twint

    # Configure
    c = twint.Config()
    c.Username = "klenwell"
    c.Store_object = True

    # Run
    twint.run.Favorites(c)
    faves = twint.output.tweets_list
    print(len(faves))
    print(faves[0], faves[-1])

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
    else:
        usage()


#
# Main
#
if __name__ == '__main__':
    controller()
