from celery import shared_task

from src.aggregates.profile.services import profile_service
from src.apps.engagement_discovery.engagement_discovery_objects import \
  deserialize_engagement_opportunity_discovery_object


@shared_task
def save_profile_from_provider_info_task(profile_external_id, provider_type):

  return profile_service.save_profile_from_provider_info(profile_external_id, provider_type).id
