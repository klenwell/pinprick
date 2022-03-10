from datetime import date

from mailers.gmail_api_mailer import GmailApiMailer
from mailers.helpers import format_bookmark_section
from services.bookmark_service import distributed_sample, by_created_on_day


class DailyMailer(GmailApiMailer):
    def __init__(self):
        subject = 'Pinprick Daily Mailer'
        body = self.compose_body()
        super().__init__(subject=subject, body=body)

    #
    # Instance Methods
    #
    def compose_body(self):
        today = date.today()
        archive_bookmarks = distributed_sample(5)
        this_day_bookmarks = by_created_on_day(today.month, today.day)
        return self.format_html_body(archive_bookmarks, this_day_bookmarks)

    def format_html_body(self, archive_bookmarks, this_day_bookmarks):
        email_f = """
<h2>Daily Bookmarks</h2>
{}
{}
"""

        archive_section = format_bookmark_section('From the Archives', archive_bookmarks)
        this_day_section = format_bookmark_section('Bookmarked This Day', this_day_bookmarks)
        return email_f.format(archive_section, this_day_section)
