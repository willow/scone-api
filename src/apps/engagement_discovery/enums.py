from enum import IntEnum
import re
from src.libs.web_utils.url.url_utils import normalize_url
from urllib.parse import urlparse


class ProviderEnum(IntEnum):
  twitter = 1
  reddit = 2
  linkedin = 3

  @staticmethod
  def get_from_url(url):
    url = normalize_url(url)

    parsed_url = urlparse(url)
    for provider in ProviderEnum:
      if provider.name.lower() in parsed_url.netloc:
        return provider
    else:
      raise ValueError("Invalid url. No provider matches the url")


ProviderChoices = (
  (ProviderEnum.twitter.value, 'Twitter'),
  (ProviderEnum.reddit.value, 'Reddit'),
  (ProviderEnum.linkedin.value, 'LinkedIn')
)


class ProviderActionEnum(IntEnum):
  twitter_tweet = 1
  reddit_comment = 2
  reddit_self_post = 3
  reddit_link_post = 4


ProviderActionChoices = (
  (ProviderActionEnum.twitter_tweet.value, 'Tweet'),
  (ProviderActionEnum.reddit_comment.value, 'Reddit Comment'),
  (ProviderActionEnum.reddit_self_post.value, 'Reddit Self Post'),
  (ProviderActionEnum.reddit_link_post.value, 'Reddit Link Post'),
)
