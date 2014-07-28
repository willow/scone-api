from enum import IntEnum


class TopicCategoryEnum(IntEnum):
  twitter_search = 1
  subreddit = 2
  keywords = 3

TopicCategoryChoices = (
  (TopicCategoryEnum.twitter_search.value, 'twitter search'),
  (TopicCategoryEnum.subreddit.value, 'subreddit'),
  (TopicCategoryEnum.keywords.value, 'keywords'),
)
