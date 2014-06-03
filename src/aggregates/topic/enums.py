from enum import IntEnum


class TopicCategoryEnum(IntEnum):
  hashtag = 1
  subreddit = 2

TopicCategoryChoices = (
  (TopicCategoryEnum.hashtag.value, 'hashtag'),
  (TopicCategoryEnum.subreddit.value, 'subreddit'),
)
