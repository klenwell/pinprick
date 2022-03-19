"""
Collect favorites from Twitter account.

USAGE:
    python main.py usage
"""
import sys
import random


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
    raise("Waiting for Twitter API access approval.")


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


def test_api():
    import tweepy
    from config.secrets import TWITTER

    # https://docs.tweepy.org/en/latest/authentication.html
    # NOTE: This does not work. Error:
    # tweepy.errors.TweepyException: Expected token_type to equal "bearer", but got None instead
    # auth = tweepy.OAuth2AppHandler(
    #     TWITTER['consumer-key'], TWITTER['consumer-secret']
    # )
    # api = tweepy.API(auth)
    # public_tweets = api.home_timeline()
    # breakpoint()
    # return

    # Collect my favorites
    auth = tweepy.OAuth1UserHandler(
        TWITTER['consumer-key'], TWITTER['consumer-secret'], TWITTER['access-token'],
        TWITTER['access-secret']
    )

    api = tweepy.API(auth)

    cursor_params = {
        'id': 'me',
        'wait_on_rate_limit': True,
        'count': 200
    }

    pages = 0

    # https://stackoverflow.com/q/39840571/1093087
    for page in tweepy.Cursor(api.get_favorites, **cursor_params).pages(50):
        pages += 1
        for fave in page:
            faves.append(fave)

    anniversary_faves = filter_faves_by_todays_date(faves)
    mailer = GmailSmtpMailer(anniversary_faves)
    mailer.deliver_to(my_email_address)

    print(pages, len(faves), faves[0], faves[-1])

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
