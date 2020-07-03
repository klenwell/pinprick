"""
Email random bookmarks from a Pinboard Account.

USAGE:
    python main.py usage
"""
import sys
import random

from services.bookmark_service import BookmarkService
from mailers.mailer import Mailer


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
    num_bookmarks = 5
    subject = 'Pinprick Daily Mailer'
    recipient = args[1]

    bookmarks = BookmarkService.import_all()
    random_bookmarks = random.sample(bookmarks, num_bookmarks)

    mailer = Mailer(random_bookmarks, subject=subject)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))


# Usage: python main.py music_mailer <email>
def music_mailer(args):
    tags = ['music', 'youtube']
    num_bookmarks = 3
    subject = 'Pinprick Music Mailer'
    recipient = args[1]

    bookmarks = BookmarkService.import_by_tags(tags)
    random_bookmarks = random.sample(bookmarks, num_bookmarks)

    mailer = Mailer(random_bookmarks, subject=subject)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))


# Usage: python main.py interactive
def interactive():
    from datetime import date
    today = date.today()
    pinboard = BookmarkService()
    created_today = [b for b in pinboard.bookmarks if b.is_created_this_day(today.month, today.day)]

    print("Loaded %s bookmarks" % (len(created_today)))
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
