from unittest.mock import MagicMock

import pytest
from twython.api import Twython

from src.libs.social_utils.providers.twitter import twitter_client_service


@pytest.mark.parametrize(("keywords", "ret_val"), [
  (['python'], 'python'),
  (['python', 'twitter'], 'python OR twitter'),
])
def test_twitter_service_joins_keywords(keywords, ret_val):
  twitter_client_mock = MagicMock(spec=Twython)

  twitter_client_mock.search = MagicMock(
    return_value=[]
  )

  twitter_click_provider_mock = MagicMock()
  twitter_click_provider_mock.get_twitter_client.return_value = twitter_client_mock

  twitter_client_service.search_twitter_by_keywords(*keywords, _twitter_client_provider=twitter_click_provider_mock)
  assert ret_val == twitter_client_mock.search.call_args_list[0][1]['q']


def test_twitter_service_excludes_retweets():
  twitter_client_mock = MagicMock(spec=Twython)

  twitter_client_mock.search = MagicMock(
    return_value=[]
  )

  twitter_click_provider_mock = MagicMock()
  twitter_click_provider_mock.get_twitter_client.return_value = twitter_client_mock

  twitter_client_service.search_twitter_by_keywords('python', exclude_retweets=True,
                                            _twitter_client_provider=twitter_click_provider_mock)

  assert '+exclude:retweets -"rt" -"mt" python' == twitter_client_mock.search.call_args_list[0][1]['q']
