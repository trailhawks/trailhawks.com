import feedparser
from dateutil.parser import parse
from dateutil.tz import gettz
from django.template import Library

from core import __version__

register = Library()


@register.simple_tag(takes_context=True)
def get_latest_tweets(context):
    try:
        d = feedparser.parse("https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=trailhawks")
        raw_tweets = d["entries"][:4]
        tweets = []
        for tweet in raw_tweets:
            text = tweet["title"].replace("trailhawks: ", "")
            date = parse(tweet["updated"])
            data = {}
            data["text"] = text
            data["url"] = tweet["link"]
            data["pub_time"] = date.astimezone(gettz())
            tweets.append(data)
        return tweets

    except Exception:
        return


@register.simple_tag(takes_context=True)
def get_rrca_news(context):
    try:
        d = feedparser.parse("http://feeds.feedburner.com/RRCA-News?format=xml")
        return d["entries"][:4]

    except Exception:
        return


@register.simple_tag(takes_context=True)
def get_version(context):
    return __version__


@register.inclusion_tag("includes/facebook_like.html", takes_context=True)
def render_facebook_like(context, obj):
    return {
        "object": obj,
    }
