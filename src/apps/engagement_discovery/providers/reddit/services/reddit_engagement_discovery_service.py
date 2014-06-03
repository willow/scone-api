import logging
from src.apps.engagement_discovery.engagement_discovery_objects import EngagementOpportunityDiscoveryObject
from src.apps.engagement_discovery.providers.reddit.services import reddit_client_service
from src.apps.engagement_discovery.signals import engagement_opportunity_discovered

logger = logging.getLogger(__name__)


def _find_reddit_eos_from_subreddit(subtopic_name, _reddit_client_service=None):
  if not _reddit_client_service: _reddit_client_service = reddit_client_service
  submissions = _reddit_client_service.search_by_subreddit(subtopic_name)
  return submissions


def discover_engagement_opportunities_from_subreddit(subtopic):
  logger.debug('beginning discovery for subtopic %s', subtopic)

  reddit_eos = _find_reddit_eos_from_subreddit(subtopic.subtopic_name)

  for reddit_eo in reddit_eos:
    username = reddit_eo.username
    eo_text = reddit_eo.reddit_obj_attrs['text']

    discovery_object = EngagementOpportunityDiscoveryObject(
      username,
      reddit_eo.reddit_obj_id,
      reddit_eo.reddit_obj_attrs,
      reddit_eo.created_date,
      reddit_eo.provider_type,
      reddit_eo.provider_action_type,
      subtopic.topic.id
    )

    logger.debug('sending discovery object. Redditor: %s. Reddit EO: %s', username, eo_text)

    engagement_opportunity_discovered.send(
      EngagementOpportunityDiscoveryObject,
      engagement_opportunity_discovery_object=discovery_object)

  logger.debug('finished discovery for subtopic %s', subtopic)
