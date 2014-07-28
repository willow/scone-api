from src.libs.social_utils.providers.reddit import reddit_client_provider


def search_by_redditor(author, _reddit_client_provider=None):
  if not _reddit_client_provider: _reddit_client_provider = reddit_client_provider
  reddit_client = _reddit_client_provider.get_reddit_client()

  return reddit_client.get_redditor(author)
