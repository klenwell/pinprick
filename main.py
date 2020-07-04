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
    from services.bookmark_lottery_service import shard_list, choose_randomly_distributed_bookmarks

    today = date.today()
    pinboard = BookmarkService()
    bookmarks = pinboard.bookmarks

    created_today = [b for b in pinboard.bookmarks if b.is_created_this_day(today.month, today.day)]
    print("Loaded %s bookmarks" % (len(created_today)))

    year_counts = {}
    for bookmark in bookmarks:
        year = bookmark.created_at.year
        count = year_counts.get(year, 0)
        year_counts[year] = count + 1
    print(year_counts)

    bookmark_shards = shard_list(bookmarks, 5)
    shard_bounds = [(shard[0].created_at, shard[-1].created_at) for shard in bookmark_shards]
    print(shard_bounds)

    selected_bookmarks = choose_randomly_distributed_bookmarks(5)
    print([b.created_at.year for b in selected_bookmarks])

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
