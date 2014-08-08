from celery import shared_task

from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.aggregates.topic.services import topic_service
from src.apps.engagement_discovery.engagement_discovery_objects import \
  deserialize_engagement_opportunity_discovery_object

import logging
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@shared_task
def create_engagement_opportunity_task(profile_id, engagement_opportunity_discovery_object):
  engagement_opportunity_discovery_object = deserialize_engagement_opportunity_discovery_object(
    engagement_opportunity_discovery_object
  )

  eo_log_message = (
    "Begin add eo. profile_id: %s, eo_external_id: %s",
    profile_id, engagement_opportunity_discovery_object.engagement_opportunity_external_id
  )

  with log_wrapper(logger.debug, *eo_log_message):
    profile = profile_service.get_profile(profile_id)

    ret_val = engagement_opportunity_service.get_engagement_opportunity_from_engagement_discovery(
      profile, engagement_opportunity_discovery_object
    ).id

  return ret_val


@shared_task
def add_topic_to_engagement_opportunity_task(engagement_opportunity_id, topic_id):
  eo_topic_log_message = (
    "Begin add eo topic. eo_id: %s, topic_id: %s",
    engagement_opportunity_id, topic_id
  )

  with log_wrapper(logger.debug, *eo_topic_log_message):
    engagement_opportunity = engagement_opportunity_service.get_engagement_opportunity(engagement_opportunity_id)
    topic = topic_service.get_topic(topic_id)

    ret_val = engagement_opportunity_service.add_topic_to_engagement_opportunity(engagement_opportunity, topic).id

  return ret_val
