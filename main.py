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
# Main Commands
#
def main():
    args = sys.argv[1:]
    command = args[0] if args else None

    print('Command: %s / Arguments: %s' % (command, args))

    if command == 'interactive':
        interactive()
    elif command == 'mail':
        mail_bookmarks(args)
    else:
        usage()

def usage():
    USAGE = """
USAGE

To experiment with command line:
    python main.py interactive

To send email:
    python main.py mail <user>@example.com
"""
    print(USAGE)

def interactive():
    bookmarks = BookmarkService.import_all()
    print("Loaded %s bookmarks" % (len(bookmarks)))
    pdb.set_trace()

def mail_bookmarks(args):
    NUM_BOOKMARKS = 5
    recipient = args[1]

    bookmarks = BookmarkService.import_all()
    random_bookmarks = random.sample(bookmarks, NUM_BOOKMARKS)

    mailer = Mailer(random_bookmarks)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))

#
# Main
#
if __name__ == '__main__':
    main()
