from django.conf import settings
from twython import Twython

_twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)


def get_twitter_client():
  return _twitter
