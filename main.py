"""
Email random bookmarks from a Pinboard Account.

USAGE:
    python main.py usage
"""
import sys
import random

from services.bookmark_service import BookmarkService
from mailers.daily_mailer import DailyMailer
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

    mailer = Mailer(random_bookmarks, subject=subject)
    mailer.deliver_to(recipient)
    print('Message delivered to {}'.format(recipient))


# Usage: python main.py interactive
def interactive():
    # pinboard = BookmarkService()
    # print(len(pinboard.bookmarks))
    import os.path
    import base64
    from email.mime.text import MIMEText
    from datetime import datetime

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    from config.secrets import GMAIL

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    # Create Service
    creds = None
    my_email = '{}@gmail.com'.format(GMAIL['address'])
    token_file = 'config/gmail-api-token.json'
    secrets_file = 'config/gmail-api-credentials.json'

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Create Message
    text_body = 'This is a test of the Gmail API using OAuth at {}'.format(datetime.now())
    message = MIMEText(text_body)
    message['to'] = my_email
    message['subject'] = 'Test Email Using Gmail API'
    message_body = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    # Send Message
    breakpoint()
    user_id = 'me'
    message = (service.users().messages().send(userId=user_id, body=message_body).execute())
    print('Message Id: {} sent to {}'.format(message['id'], my_email))


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
