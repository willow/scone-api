from src.aggregates.profile import constants
import logging
from src.libs.social_utils.providers.twitter import twitter_search_utils

logger = logging.getLogger(__name__)
_twitter_url_prefix = "https://twitter.com/{0}"


def get_twitter_profile_attrs(profile_external_id):
  return _get_twitter_profile_data(profile_external_id)


def _get_recent_tweets(user_data):
  recent_tweets = []
  for tweet in user_data:
    recent_tweets.append(tweet[constants.TEXT])
  return recent_tweets


def _get_twitter_profile_data(profile_external_id, _search=twitter_search_utils, **kwargs):
  # todo find a way to only query 1 tweet - a limit
  user_data = _search.search_twitter_by_user(profile_external_id, **kwargs)
  profile_data = user_data[0]['user']

  profile_url = _twitter_url_prefix.format(profile_external_id)
  name = profile_data['name']
  bio = profile_data['description']
  followers_count = profile_data['followers_count']
  following_count = profile_data['friends_count']
  location = profile_data['location']

  user_websites = _get_twitter_profile_websites(profile_data)

  recent_tweets = _get_recent_tweets(user_data)

  twitter_profile_data = {
    constants.PROFILE_URL: profile_url,
    constants.NAME: name, constants.FOLLOWERS_COUNT: followers_count, constants.FOLLOWING_COUNT: following_count,
    constants.RECENT_TWEETS: recent_tweets,
  }

  if bio: twitter_profile_data[constants.BIO] = bio
  if user_websites: twitter_profile_data[constants.WEBSITES] = user_websites
  if location: twitter_profile_data[constants.LOCATION] = location

  return twitter_profile_data


def _get_twitter_profile_websites(profile_data):
  user_websites = []
  try:
    entities = profile_data['entities']

    # twitter stores urls in a user's profile field `Description`.
    entity_url_key = entities.get('url')
    if entity_url_key:
      urls = entity_url_key.get('urls', [])
      user_websites.extend(x['expanded_url'] for x in urls)

    # twitter ALSO stores urls in a user's profile field `URL`.
    # So a user might store urls in their description field or the pre-defined field for links.
    entity_description_key = entities.get('description')
    if entity_description_key:
      urls = entity_description_key.get('urls', [])
      user_websites.extend(x['expanded_url'] for x in urls)

  except KeyError as e:
    logger.debug(e)
  return user_websites
