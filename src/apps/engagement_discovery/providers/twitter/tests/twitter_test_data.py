import datetime
import pytz


eastern_time_zone = pytz.timezone('US/Eastern')

# region tweet1
tweet_1_base_tweet_1 = {
  "in_reply_to_user_id": None,
  "retweet_count": 0,
  "favorite_count": 0,
  "user": {
    "statuses_count": 100,
    "followers_count": 1000,
    "friends_count": 1000,
  },
}

tweet_1_reply_tweet_1 = dict(
  tweet_1_base_tweet_1,
  in_reply_to_user_id=123
)

tweet_1_reply_tweet_2 = dict(
  tweet_1_base_tweet_1,
  in_reply_to_user_id=None
)

tweet_1_favorite_tweet_1 = dict(
  tweet_1_base_tweet_1,
  favorite_count=123
)

tweet_1_favorite_tweet_2 = dict(
  tweet_1_base_tweet_1,
  favorite_count=1
)

tweet_1_user_status_1 = dict(
  tweet_1_base_tweet_1,
  user=dict(tweet_1_base_tweet_1["user"], statuses_count=10)
)

tweet_1_user_status_2 = dict(
  tweet_1_base_tweet_1,
  user=dict(tweet_1_base_tweet_1["user"], statuses_count=100)
)

tweet_1_user_following_ratio_1 = dict(
  tweet_1_base_tweet_1,
  user=dict(
    tweet_1_base_tweet_1["user"],
    followers_count=1000,
    friends_count=100,
  )
)

tweet_1_user_following_ratio_2 = dict(
  tweet_1_base_tweet_1,
  user=dict(
    tweet_1_base_tweet_1["user"],
    followers_count=1000,
    friends_count=1000,
  )
)

# endregion tweet1

# region tweet2
tweet_2_base_tweet_1 = {
  "created_at": str(datetime.datetime.now(eastern_time_zone)),
  "text": "This is a tweet",
  "id_str": "12345",
  "in_reply_to_user_id": None,
  "retweet_count": 0,
  "favorite_count": 0,
  "user": {
    "statuses_count": 100,
    "followers_count": 1000,
    "friends_count": 1000,
    "screen_name": "test_user_2",
    "name": "test_user_2",
    "description": "This is a description",
    "location": "NYC",
  },
}


# endregion tweet2
