from enum import IntEnum


class ProviderEnum(IntEnum):
  twitter = 1
  reddit = 2


ProviderChoices = (
  (ProviderEnum.twitter.value, 'Twitter'),
  (ProviderEnum.reddit.value, 'Reddit'),
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
