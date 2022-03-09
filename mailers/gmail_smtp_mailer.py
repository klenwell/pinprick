"""
**Google has deprecated and will soon disable this method.**

More info here: https://support.google.com/accounts/answer/6010255

For mailing, use the new GmailApiMailer class. This class has been kept only to serve
as a reference.
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.secrets import GMAIL


SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
DEFAULT_SUBJECT = 'Pinprick Bulletin'


class GmailSmtpMailer:
    def __init__(self, **keywords):
        self.subject = keywords.get('subject', DEFAULT_SUBJECT)
        self.body = keywords.get('body', '(No body)')

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
            smtp.send_message(message)

        return message

    def build_mime_multipart_message(self, recipient):
        message = MIMEMultipart('alternative')
        message['From'] = '{} <{}>'.format(self.from_name, GMAIL['address'])
        message['To'] = recipient
        message['Subject'] = self.subject

        message.attach(MIMEText(self.body, 'html'))
        return message
