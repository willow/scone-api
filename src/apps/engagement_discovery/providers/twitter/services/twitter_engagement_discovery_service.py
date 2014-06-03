import logging

from src.apps.engagement_discovery.engagement_discovery_objects import EngagementOpportunityDiscoveryObject
from src.apps.engagement_discovery.enums import ProviderEnum
from src.apps.engagement_discovery.providers.twitter.services import twitter_client_service
from src.apps.engagement_discovery.signals import engagement_opportunity_discovered


logger = logging.getLogger(__name__)


def discover_engagement_opportunities_from_tweets(subtopic, _twitter_client_service=None):
  if not _twitter_client_service: _twitter_client_service = twitter_client_service
  logger.debug('beginning discovery for subtopic %s', subtopic)

  twitter_eos = _twitter_client_service.find_tweets_from_keyword(subtopic.subtopic_name)

  for twitter_eo in twitter_eos:
    discovery_object = EngagementOpportunityDiscoveryObject(
      twitter_eo.username,
      twitter_eo.twitter_obj['id_str'],
      twitter_eo.twitter_obj_attrs,
      twitter_eo.created_date,
      twitter_eo.provider_type,
      twitter_eo.provider_action_type,
      subtopic.topic_id
    )

    logger.debug('sending discovery object. Username: %s. Tweet: %s', twitter_eo.username,
                 twitter_eo.twitter_obj['text'])

    engagement_opportunity_discovered.send(
      EngagementOpportunityDiscoveryObject,
      engagement_opportunity_discovery_object=discovery_object)

  logger.debug('finished discovery for subtopic %s', subtopic)
