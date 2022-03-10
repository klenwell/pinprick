"""
Email random bookmarks from a Pinboard Account.

USAGE:
    python main.py usage
"""
import sys
import random

from services.bookmark_service import BookmarkService
from mailers.daily_mailer import DailyMailer
from mailers.gmail_api_mailer import GmailApiMailer


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

    mailer = GmailApiMailer(random_bookmarks, subject=subject)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))


# Usage: python main.py interactive
def interactive():
    # pinboard = BookmarkService()
    # print(len(pinboard.bookmarks))
    from datetime import datetime
    from config.secrets import GMAIL

    recipient = '{}@gmail.com'.format(GMAIL['address'])
    subject = 'Test Email Using Gmail API'
    body = 'This is a test of the Gmail API using OAuth at {}'.format(datetime.now())

    mailer = GmailApiMailer(subject=subject, body=body)
    message = mailer.deliver_to(recipient)
    print('Message Id: {} sent to {}'.format(message['id'], recipient))

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
    else:
        usage()


#
# Main
#
if __name__ == '__main__':
    controller()
