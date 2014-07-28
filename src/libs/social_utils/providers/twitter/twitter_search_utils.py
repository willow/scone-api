import datetime
from dateutil.relativedelta import relativedelta
from src.libs.social_utils.providers.twitter import twitter_client_provider


_EXCLUDE_RT = '+exclude:retweets -"rt" -"mt"'


def get_time_period_back(since):
  since = since.lower()
  if since == "w":
    relative_delta = {"weeks": 1}
  elif since == "d":
    relative_delta = {"days": 1}
  else:
    raise ValueError("invalid since value")

  since_date_range = (datetime.datetime.utcnow() - relativedelta(**relative_delta)).strftime("%Y-%m-%d")
  return since_date_range


def search_twitter_by_user(screen_name,
                           since=None,
                           lang="en",
                           count=50, _twitter_client_provider=twitter_client_provider):
  client = _twitter_client_provider.get_twitter_client()

  search_params = {"lang": lang, "count": count}

  search_params["screen_name"] = screen_name

  if since:
    search_params["since"] = get_time_period_back(since)

  return client.get_user_timeline(**search_params)


def search_twitter(query,
                   screen_name=None,
                   geocode=None,
                   exclude_retweets=False, since=None,
                   lang="en", include_entities=False, count=100, result_type='recent',
                   _twitter_client_provider=twitter_client_provider):
  client = _twitter_client_provider.get_twitter_client()

  search_params = {"lang": lang, "include_entities": include_entities, "count": count, "result_type": result_type}

  if exclude_retweets:
    query = "{0} {1}".format(_EXCLUDE_RT, query)

  if screen_name:
    search_params["from"] = screen_name
    
  if geocode:
    search_params["geocode"] = geocode

  search_params["q"] = query

  if since:
    search_params["since"] = get_time_period_back(since)

  return client.search(**search_params)
