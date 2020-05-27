"""
Email random bookmarks from a Pinboard Account.

USAGE:
    python main.py usage
"""
import sys, pdb
import random

from models.bookmark import Bookmark
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

def daily_mailer(args):
    num_bookmarks = 5
    subject = 'Daily Pinboard Bulletin'
    recipient = args[1]

    bookmarks = BookmarkService.import_all()
    random_bookmarks = random.sample(bookmarks, num_bookmarks)

    mailer = Mailer(random_bookmarks, subject=subject)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))

def interactive():
    bookmarks = BookmarkService.import_all()
    print("Loaded %s bookmarks" % (len(bookmarks)))
    pdb.set_trace()


#
# Main Commands
#
def main():
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
    main()
