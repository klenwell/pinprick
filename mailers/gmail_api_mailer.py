import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import cached_property

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


DEFAULT_SUBJECT = 'Pinprick Bulletin'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'config/gmail-api-token.json'
CREDS_FILE = 'config/gmail-api-credentials.json'


class GmailApiMailer:
    #
    # Static Methods
    #
    def refresh_api_credentials():
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        return creds

    #
    # Properties
    #
    @cached_property
    def gmail_api_service(self):
        """Source:
        https://developers.google.com/gmail/api/quickstart/python#step_2_configure_the_sample
        """
        creds = GmailApiMailer.refresh_api_credentials()
        return build('gmail', 'v1', credentials=creds)

    #
    # Instance Methods
    #
    def __init__(self, **keywords):
        self.subject = keywords.get('subject', DEFAULT_SUBJECT)
        self.body = keywords.get('body', '(No body)')
        self.from_name = 'Pinprick Bot'

    def deliver_to(self, recipient):
        user_id = 'me'
        message = self.build_mime_multipart_message(recipient)
        service = self.gmail_api_service
        return (service.users().messages().send(userId=user_id, body=message).execute())

    def build_mime_multipart_message(self, recipient):
        message = MIMEMultipart('alternative')
        message['To'] = recipient
        message['Subject'] = self.subject

        message.attach(MIMEText(self.body, 'html'))
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
