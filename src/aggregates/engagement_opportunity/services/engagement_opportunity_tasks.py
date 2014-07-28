from celery import shared_task

from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.aggregates.topic.services import topic_service
from src.apps.engagement_discovery.engagement_discovery_objects import \
  deserialize_engagement_opportunity_discovery_object

import logging

logger = logging.getLogger(__name__)


@shared_task
def create_engagement_opportunity_task(profile_id, engagement_opportunity_discovery_object):
  engagement_opportunity_discovery_object = deserialize_engagement_opportunity_discovery_object(
    engagement_opportunity_discovery_object
  )

  logger.debug(
    "Begin add eo. profile_id: %s, eo_external_id: %s",
    profile_id, engagement_opportunity_discovery_object.engagement_opportunity_external_id
  )

  profile = profile_service.get_profile(profile_id)

  ret_val = engagement_opportunity_service.get_engagement_opportunity_from_engagement_discovery(
    profile, engagement_opportunity_discovery_object
  ).id

  logger.debug(
    "Completed add eo. profile_id: %s, eo_external_id: %s",
    profile_id, engagement_opportunity_discovery_object.engagement_opportunity_external_id
  )

  return ret_val


@shared_task
def add_topic_to_engagement_opportunity_task(engagement_opportunity_id, topic_id):
  logger.debug(
    "Begin add eo topic. eo_id: %s, topic_id: %s",
    engagement_opportunity_id, topic_id
  )

  engagement_opportunity = engagement_opportunity_service.get_engagement_opportunity(engagement_opportunity_id)
  topic = topic_service.get_topic(topic_id)

  ret_val = engagement_opportunity_service.add_topic_to_engagement_opportunity(engagement_opportunity, topic).id

  logger.debug(
    "Completed add eo topic. eo_id: %s, topic_id: %s",
    engagement_opportunity_id, topic_id
  )

  return ret_val
