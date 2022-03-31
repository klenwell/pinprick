from datetime import date

from mailers.gmail_smtp_mailer import GmailSmtpMailer
from services.tweet_service import TweetService


class DailyTweetMailer(GmailSmtpMailer):
    def __init__(self):
        subject = 'Pinprick Daily Mailer'
        body = self.compose_body()
        super().__init__(subject=subject, body=body)

    #
    # Instance Methods
    #
    def compose_body(self):
        today = date.today()
        api = TweetService()
        random_faves = api.faves_sharded_sample(5)
        this_day_faves = api.faves_by_date(today)
        return self.format_html_body(random_faves, this_day_faves)

    def format_html_body(self, archive_bookmarks, this_day_bookmarks):
        email_f = """
<h2>Today's Tweets</h2>
{}
{}
"""

        archive_section = self.format_section('From the Archives', archive_bookmarks)
        this_day_section = self.format_section('Tweeted This Day', this_day_bookmarks)
        return email_f.format(archive_section, this_day_section)

    def format_section(self, title, tweets):
        html_f = """\
<div class="section" style="margin-bottom:8px">
  <h3>{} ({})</h3>
  {}
</div>
"""

        tweet_divs = [self.format_tweet(tweet) for tweet in tweets]
        tweet_list = "\n".join(tweet_divs)
        return html_f.format(title, len(tweets), tweet_list)

    def format_tweet(self, tweet):
        bookmark_f = """\
<div class="bookmark" style="margin-bottom:16px">
  <div class="text" style="margin-bottom:0px">
    {}
  </div>
  <div class="footer">
    <a href="{}">{}</a> &bull; <a href="{}">{}</a>
  </div>
</div>"""

        user_url = 'https://twitter.com/{}'.format(tweet.user.screen_name)
        link_url = '{}/status/{}'.format(user_url, tweet.id_str)

        return bookmark_f.format(tweet.full_text,
                                 user_url,
                                 tweet.user.screen_name,
                                 link_url,
                                 str(tweet.created_at)[:19])
