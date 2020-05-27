import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.secrets import GMAIL
from mailers.helpers import format_bookmark


SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
DEFAULT_SUBJECT = 'Daily Pinboard Bulletin'


class Mailer:
    def __init__(self, bookmarks, **keywords):
        self.bookmarks = bookmarks
        self.subject = keywords.get('subject', DEFAULT_SUBJECT)
        self.from_name = 'Pinprick Bot'
        self.smtp_address = GMAIL['address']
        self.smtp_pass = GMAIL['password']

    #
    # Instance Methods
    #
    def deliver_to(self, recipient):
        message = self.build_mime_multipart_message(recipient)

        # Connect to SMTP server.
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            # Encrypts the connection.
            smtp.starttls()

            # Log in and send email.
            smtp.login(self.smtp_address, self.smtp_pass)
            response = smtp.send_message(message)

        return message

    def build_mime_multipart_message(self, recipient):
        message = MIMEMultipart('alternative')
        message['From'] = '{} <{}>'.format(self.from_name, GMAIL['address'])
        message['To'] = recipient
        message['Subject'] = self.subject

        html_body = self.format_html_body(self.bookmarks)
        message.attach(MIMEText(html_body, 'html'))
        return message

    def format_html_body(self, bookmarks):
        email_f = """
<h3>{} Bookmarks</h3>

{}
"""
        bookmark_blocks = [format_bookmark(bookmark) for bookmark in bookmarks]
        bookmark_block = "\n".join(bookmark_blocks)
        return email_f.format(len(bookmarks), bookmark_block)
