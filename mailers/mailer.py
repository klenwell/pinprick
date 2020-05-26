import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.secrets import GMAIL


SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587


class Mailer:
    def __init__(self, bookmarks):
        self.bookmarks = bookmarks
        self.subject = 'Daily Pinboard Bulletin'
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
        bookmark_blocks = [self.format_bookmark(bookmark) for bookmark in bookmarks]
        bookmark_block = "\n".join(bookmark_blocks)
        return email_f.format(len(bookmarks), bookmark_block)

    def format_bookmark(self, bookmark):
        bookmark_f = """\
<div class="bookmark" style="margin-bottom:4px">
  <h4 style="margin-bottom:4px">
    <a href="{}">{}</a>
  </h4>
  <div class="tags">
    {}
  </div>
  <div class="meta">
    {}
  </div>
</div>"""

        def format_tags(bookmark):
            tag_blocks = [format_tag(bookmark, tag) for tag in bookmark.tags]
            return ', '.join(tag_blocks)

        def format_tag(bookmark, tag):
            tag_f = '<a href="{}">{} ({})</a>'
            return tag_f.format(bookmark.tag_to_url(tag), tag.name, tag.count)

        def format_meta(bookmark):
            meta_f = '<span>{}</span> &bull; <a href="{}">{}</a>'
            return meta_f.format(bookmark.created_at, bookmark.service_url, bookmark.service_url)

        return bookmark_f.format(bookmark.url,
                                 bookmark.title,
                                 format_tags(bookmark),
                                 format_meta(bookmark))
