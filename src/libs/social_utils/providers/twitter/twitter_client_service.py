from itertools import chain
from src.libs.python_utils.collections.iter_utils import chunks
from src.libs.social_utils.providers.twitter import twitter_search_utils


def _join_keywords(keywords):
  query = " OR ".join(k.strip() for k in keywords)
  return query


def search_by_users(*usernames, **kwargs):
  def chunk_search_by_users(chunk):
    from_usernames = ["from:" + un for un in chunk]

    query = _join_keywords(from_usernames)

    return query

  return _search_chunks(*usernames, action=chunk_search_by_users, **kwargs)


def search_twitter_by_keywords(*keywords, **kwargs):
  def chunk_search_by_keywords(chunk):
    return _join_keywords(chunk)

  return _search_chunks(*keywords, action=chunk_search_by_keywords, **kwargs)


def _search_chunks(*query_items, action, _search=twitter_search_utils, **kwargs):
  query_chunks = list(chunks(query_items, 10))

  query_chunks = [action(chunk) for chunk in query_chunks]  
  
  ret_val = [_search.search_twitter(query, **kwargs) for query in query_chunks]

  return chain.from_iterable(x['statuses'] for x in ret_val)


def get_twitter_profile_external_id(url):
  # for now, just assume it's a normal twitter url - i.e. it doesn't contain a status
  return url.rsplit('/', 1)[-1]
