import pytest

from src.apps.engagement_discovery.providers.twitter.services import twitter_client_service
from src.apps.engagement_discovery.providers.twitter.tests import twitter_test_data


@pytest.mark.parametrize(("tweet", "ret_val"), [
  (twitter_test_data.tweet_1_reply_tweet_1, False),
  (twitter_test_data.tweet_1_reply_tweet_2, True),
])
def test_tweet_with_reply_is_discarded(tweet, ret_val):
  assert ret_val == twitter_client_service._is_valid_tweet(tweet)


@pytest.mark.parametrize(("tweet", "ret_val"), [
  (twitter_test_data.tweet_1_favorite_tweet_1, False),
  (twitter_test_data.tweet_1_favorite_tweet_2, True),
])
def test_tweet_with_too_many_favorites_discarded(tweet, ret_val):
  assert ret_val == twitter_client_service._is_valid_tweet(tweet)


@pytest.mark.parametrize(("tweet", "ret_val"), [
  (twitter_test_data.tweet_1_user_status_1, False),
  (twitter_test_data.tweet_1_user_status_2, True),
])
def test_tweet_with_too_few_tweets_discarded(tweet, ret_val):
  assert ret_val == twitter_client_service._is_valid_tweet(tweet)


@pytest.mark.parametrize(("tweet", "ret_val"), [
  (twitter_test_data.tweet_1_user_following_ratio_1, False),
  (twitter_test_data.tweet_1_user_following_ratio_2, True),
])
def test_tweet_with_too_low_ratio_discarded(tweet, ret_val):
  assert ret_val == twitter_client_service._is_valid_tweet(tweet)
