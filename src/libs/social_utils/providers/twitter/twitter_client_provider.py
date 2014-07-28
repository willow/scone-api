from twython import Twython
from django.conf import settings

_twitter = Twython(
  settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET,
  client_args={'timeout': settings.HTTP_TIMEOUT}
)


def get_twitter_client():
  return _twitter
