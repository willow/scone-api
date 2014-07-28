import logging
from src.aggregates.profile.services import profile_service

from src.apps.engagement_discovery.engagement_discovery_objects import EngagementOpportunityDiscoveryObject
from src.apps.engagement_discovery.providers.twitter.services import twitter_client_service
from src.apps.engagement_discovery.signals import engagement_opportunity_discovered
from src.libs.nlp_utils.services.enums import NamedEntityTypeEnum


logger = logging.getLogger(__name__)


def discover_engagement_opportunities_from_twitter_subtopic(subtopic, _twitter_client_service=None,
                                                            **kwargs):
  if not _twitter_client_service: _twitter_client_service = twitter_client_service
  logger.debug('beginning discovery for subtopic %s', subtopic)

  # this is if we want to limit eo discover by username
  profile_id = kwargs.pop('profile_id', None)
  if profile_id:
    profile = profile_service.get_profile(profile_id)
    kwargs['screen_name'] = profile.profile_external_id

  # if we want to get additional parameters (like geocode, since, follower count)
  geocode = subtopic.subtopic_attrs.get('geocode')
  if geocode:
    kwargs['geocode'] = geocode

  since = subtopic.subtopic_attrs.get('since', 'd')
  kwargs['since'] = since

  named_entity_type = subtopic.subtopic_attrs.get('named_entity_type')
  if named_entity_type:
    named_entity_type = NamedEntityTypeEnum[named_entity_type]
  else:
    named_entity_type = NamedEntityTypeEnum.person

  twitter_eos = _twitter_client_service.find_tweets_from_keyword(subtopic.subtopic_name, named_entity_type, **kwargs)

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
