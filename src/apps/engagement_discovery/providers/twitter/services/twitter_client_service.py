from itertools import groupby

from src.aggregates.profile.models import Profile
from src.apps.engagement_discovery import constants
from src.apps.engagement_discovery.providers.twitter.twitter_engagement_discovery_objects import \
  TwitterEngagementOpportunityDiscoveryObject
from src.libs.datetime_utils.parsers import datetime_parser
from src.libs.nlp_utils.services import named_entity_service
from src.libs.nlp_utils.services.enums import NamedEntityTypeEnum
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.social_utils.providers.twitter import twitter_client_service

from src.aggregates.profile.services.profile_service import get_profile_from_provider_info
from src.apps.engagement_discovery.enums import ProviderEnum, ProviderActionEnum
import logging

logger = logging.getLogger(__name__)

_twitter_url_prefix = "https://twitter.com/{0}"


def _is_valid_tweet(tweet):
  ret_val = True

  if ret_val:
    if tweet['in_reply_to_user_id']:
      ret_val = False

  if ret_val:
    if tweet['retweet_count'] >= 20 or tweet['favorite_count'] >= 20:
      ret_val = False

  if ret_val:
    if tweet['user']['statuses_count'] < 50:
      ret_val = False

  if ret_val:
    followers_count = tweet['user']['followers_count']
    following_count = tweet['user']['friends_count']

    if following_count >= 30 and followers_count >= 30:
      if followers_count > 500:
        ret_val = (following_count / followers_count) >= .65
    else:
      ret_val = False

  return ret_val


def find_tweets_from_keyword(keyword, named_entity_type, _twitter_client_service=None, **kwargs):
  ret_val = []
  if not _twitter_client_service:
    _twitter_client_service = twitter_client_service

  search_log_message = (
    "Searching twitter for keyword: %s",
    keyword
  )

  with log_wrapper(logger.debug, *search_log_message):
    tweets_from_keywords = _twitter_client_service.search_twitter_by_keywords(
      keyword,
      include_entities=True,
      exclude_retweets=True,
      **kwargs
    )

  if kwargs.get('screen_name'):
    valid_tweets = tweets_from_keywords

  else:
    valid_tweet_log_message = (
      "Getting valid tweets for keyword: %s",
      keyword
    )

    with log_wrapper(logger.debug, *valid_tweet_log_message):

      tweets_from_keywords = [tweet for tweet in tweets_from_keywords if _is_valid_tweet(tweet)]

      usernames_from_tweets = sorted(set(tweet['user']['screen_name'] for tweet in tweets_from_keywords))

      tweets_from_users = _twitter_client_service.search_by_users(*usernames_from_tweets, since="w")

      valid_usernames = _get_valid_users_from_tweets(tweets_from_users, named_entity_type)

      valid_tweets = [tweet for tweet in tweets_from_keywords if tweet['user']['screen_name'] in valid_usernames]

  for tweet in valid_tweets:
    username = tweet['user']['screen_name']

    profile_url = _twitter_url_prefix.format(username)
    tweet_id = tweet['id_str']
    url = "{0}/status/{1}".format(profile_url, tweet_id)
    text = tweet['text']
    tweet_created_date = tweet["created_at"]
    tweet_websites = _get_tweet_websites(tweet)

    tweet_data = {
      constants.URL: url, constants.TEXT: text,
    }

    if tweet_websites: tweet_data[constants.WEBSITES] = tweet_websites

    ret_val.append(
      TwitterEngagementOpportunityDiscoveryObject(
        username,
        tweet_id,
        ProviderEnum.twitter,
        ProviderActionEnum.twitter_tweet,
        tweet,
        tweet_data,
        datetime_parser.get_datetime(tweet_created_date)
      )
    )

  return ret_val


def _get_valid_users_from_tweets(tweets_from_users, named_entity_type, _named_entity_service=None):
  if not _named_entity_service:
    _named_entity_service = named_entity_service

  ret_val = []

  name_key = lambda tweet: tweet['user']['screen_name']

  tweets_from_users = sorted(tweets_from_users, key=name_key)

  user_grouped_tweets = dict((k, list(v)) for k, v in groupby(tweets_from_users, name_key))
  active_users = {key: value for key, value in user_grouped_tweets.items() if len(value) >= 2}

  for user, tweets in active_users.items():
    valid_user = False

    if named_entity_type == NamedEntityTypeEnum.any:
      valid_user = True
    else:
      try:
        get_profile_from_provider_info(user, ProviderEnum.twitter)
        valid_user = True
      except Profile.DoesNotExist:
        name_for_user = tweets[0]['user']['name']

        try:
          if _named_entity_service.get_entity_type(name_for_user) == named_entity_type:
            valid_user = True
        except:
          logger.exception("Error getting entity type. name: %s", name_for_user)
          valid_user = False

    if valid_user:
      ret_val.append(user)

  return ret_val


def _get_tweet_websites(tweet):
  tweet_websites = []
  entities = tweet['entities']

  # twitter stores urls in a tweets's field `entities`.
  entity_urls_key = entities.get('urls', [])
  tweet_websites.extend(x['expanded_url'] for x in entity_urls_key)
  return tweet_websites
