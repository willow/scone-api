from celery import shared_task

from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.aggregates.topic.services import topic_service
from src.apps.engagement_discovery.engagement_discovery_objects import \
  deserialize_engagement_opportunity_discovery_object


@shared_task
def create_engagement_opportunity_task(profile_id, engagement_opportunity_discovery_object):
  engagement_opportunity_discovery_object = deserialize_engagement_opportunity_discovery_object(
    engagement_opportunity_discovery_object
  )

  profile = profile_service.get_profile(profile_id)

  return engagement_opportunity_service.get_engagement_opportunity_from_engagement_discovery(
    profile, engagement_opportunity_discovery_object
  ).id


@shared_task
def add_topic_to_engagement_opportunity_task(engagement_opportunity_id, topic_id):
  engagement_opportunity = engagement_opportunity_service.get_engagement_opportunity(engagement_opportunity_id)
  topic = topic_service.get_topic(topic_id)

  return engagement_opportunity_service.add_topic_to_engagement_opportunity(engagement_opportunity, topic).id
