import pytest
from src.aggregates.topic.enums import TopicCategoryEnum
from src.aggregates.topic.models import Topic
from src.apps.engagement_discovery.enums import ProviderActionEnum, ProviderEnum
from src.apps.engagement_discovery.providers.twitter.services import twitter_engagement_discovery_service, \
  twitter_client_service
from src.apps.engagement_discovery.providers.twitter.tests import twitter_test_data
from src.apps.engagement_discovery.providers.twitter.twitter_engagement_discovery_objects import \
  TwitterEngagementOpportunityDiscoveryObject
from src.libs.datetime_utils.parsers import datetime_parser
from src.libs.nlp_utils.services.enums import NamedEntityTypeEnum
from unittest.mock import MagicMock, patch


@pytest.mark.django_db
@pytest.mark.graph_db
def test_tweets_create_engagement_opportunities():
  mock_twitter_client_service = MagicMock(spec=twitter_client_service)
  python_topic = Topic._from_attrs('python')
  python_topic.associate_subtopic_with_topic('#python', TopicCategoryEnum.hashtag.value, {})

  python_topic.save()

  test_tweet = twitter_test_data.tweet_2_base_tweet_1
  twitter_eo = TwitterEngagementOpportunityDiscoveryObject(
    'twitter',
    test_tweet['id_str'],
    ProviderEnum.twitter,
    ProviderActionEnum.twitter_tweet,
    test_tweet,
    {"test_tweet_attrs": test_tweet},
    datetime_parser.get_datetime(test_tweet['created_at'])
  )

  mock_twitter_client_service.find_tweets_from_keyword = MagicMock(
    return_value=[twitter_eo]
  )

  twitter_engagement_discovery_service.discover_engagement_opportunities_from_twitter_subtopic(
    python_topic._subtopics_list[0],
    mock_twitter_client_service
  )
