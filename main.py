"""
Email random bookmarks from a Pinboard Account.

For more details, see https://trello.com/c/PLcop8eM.

USAGE:
    python main.py usage
"""
import sys, pdb
import random
import pinboard

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.services import PINBOARD_BASE_URL, PINBOARD_USER, SMTP
from config.secrets import API_TOKEN, GMAIL

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
    python main.py mail tatwell@gmail.com
"""
    print(USAGE)

def interactive():
    pb = pinboard.Pinboard(API_TOKEN)
    bookmarks = pb.posts.all()
    print("Loaded %s bookmarks as bookmarks" % (len(bookmarks)))
    pdb.set_trace()

def mail_bookmarks(args):
    NUM_BOOKMARKS = 5
    recipient = args[1]

    pb = pinboard.Pinboard(API_TOKEN)
    bookmarks = pb.posts.all()
    tags = pb.tags.get()
    tags_index = tags_to_index(tags)

    random_bookmarks = random.sample(bookmarks, NUM_BOOKMARKS)
    random_bookmarks = map_tags_to_bookmarks(random_bookmarks, tags_index)

    mail_body = format_email(random_bookmarks)
    send_email(recipient, mail_body)

#
# Helper Methods
#
def send_email(recipient, html_body):
    # Source: https://codenhagen.wordpress.com/2016/07/01/sending-html-emails-through-gmail-with-python-3/
    # Create message with headers.
    message = MIMEMultipart('alternative')
    message['From'] = '{} <{}>'.format(SMTP['from_name'], GMAIL['address'])
    message['To'] = recipient
    message['Subject'] = 'Daily Pinboard Bulletin'

    # Attach HTML body
    message.attach(MIMEText(html_body, 'html'))

    # Connect to SMTP server.
    with smtplib.SMTP(SMTP['host'], SMTP['port']) as smtp:
        # Encrypts the connection.
        smtp.starttls()

        # Logging in and sending the email:
        smtp.login(GMAIL['address'], GMAIL['password'])
        smtp.send_message(message)

def tags_to_index(tags):
    index = {}
    for tag in tags:
        index[tag.name] = tag
    return index

def map_tags_to_bookmarks(bookmarks, tags_index):
    return [map_tags_to_bookmark(bookmark, tags_index) for bookmark in bookmarks]

def map_tags_to_bookmark(bookmark, tags_index):
    bookmark_tags = []

    for tag in bookmark.tags:
        bookmark_tags.append(tags_index[tag])

    bookmark.tags = bookmark_tags
    return bookmark

def format_email(bookmarks):
    email_format = """
<h3>%s randomly selected bookmarks</h3>

%s
"""
    bookmark_blocks = [format_bookmark(bookmark) for bookmark in bookmarks]
    return email_format % (len(bookmarks), "\n".join(bookmark_blocks))

def format_bookmark(bookmark):
    bookmark_format = """\
<div class="bookmark" style="margin-bottom:4px">
  <h4 style="margin-bottom:4px">
    <a href="%s">%s</a>
  </h4>
  <div class="tags">
    %s
  </div>
  <div class="meta">
    %s
  </div>
</div>"""

    def format_tags(tags):
        tag_blocks = [format_tag(tag) for tag in tags]
        return ', '.join(tag_blocks)

    def format_tag(tag):
        tag_format = '<a href="%s/u:%s/t:%s">%s (%s)</a>'
        return tag_format % (PINBOARD_BASE_URL, PINBOARD_USER, tag.name, tag.name, tag.count)

    def format_meta(bookmark):
        return '<span>%s</span> <span>TODO: permalink</span>' % (bookmark.time)

    return bookmark_format % (bookmark.url,
                              bookmark.description,
                              format_tags(bookmark.tags),
                              format_meta(bookmark))

#
# Main
#
if __name__ == '__main__':
    main()
