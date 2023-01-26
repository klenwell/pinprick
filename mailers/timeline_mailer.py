from datetime import datetime
from mailers.gmail_smtp_mailer import GmailSmtpMailer


class TimelineMailer(GmailSmtpMailer):
    def __init__(self, tweets):
        subject = f"Twitter Timeline Mailer • {datetime.now().strftime('%Y-%m-%d')}"
        body = self.compose_body(tweets)
        super().__init__(subject=subject, body=body)

    def compose_body(self, tweets):
        email_f = """
<h2>Latest Timeline</h2>
<h4 style="margin-top:2px; margin-bottom:2px;">Period: {} to {}</h4>
<h4 style="margin-top:2px; margin-bottom:2px;">Tweets: {}</h4>
<h4 style="margin-top:2px;">Users: {}</h4>

{}
"""

        # Sort in ASC order by timestamp (basically reverse order)
        tweets = sorted(tweets, key=lambda t: t.created_at)

        start_at = tweets[0].timestamp
        end_at = tweets[-1].timestamp
        user_count = len(set([t.by for t in tweets]))
        tweet_list = self.format_tweets(tweets)
        return email_f.format(start_at, end_at, len(tweets), user_count, tweet_list)

    def format_tweets(self, tweets):
        html_f = """\
<div class="section" style="margin-bottom:8px">
  {}
</div>
"""

        tweet_divs = [self.format_tweet(tweet) for tweet in tweets]
        tweet_list = "\n".join(tweet_divs)
        return html_f.format(tweet_list)

    def format_tweet(self, tweet):
        tweet_f = """\
<div class="tweet" style="margin-bottom:16px">
  <div class="text" style="margin-bottom:0px">
    {}
  </div>
  <div class="footer">
    <a href="{}">{}</a> &bull; <a href="{}">{}</a>
  </div>
</div>"""

        return tweet_f.format(
            tweet.text,
            tweet.author_url,
            tweet.by,
            tweet.url,
            tweet.timestamp
        )
