from django.dispatch import receiver

from src.aggregates.engagement_opportunity.services import engagement_opportunity_tasks
from src.aggregates.profile.services import profile_tasks
from src.apps.engagement_discovery.engagement_discovery_objects import EngagementOpportunityDiscoveryObject
from src.apps.engagement_discovery.signals import engagement_opportunity_discovered


@receiver(engagement_opportunity_discovered, sender=EngagementOpportunityDiscoveryObject)
def created_from_engagement_opportunity_callback(sender, **kwargs):
  engagement_opportunity_discovery_object = kwargs['engagement_opportunity_discovery_object']
  (
    profile_tasks.save_profile_from_provider_info_task.s(
      engagement_opportunity_discovery_object.profile_external_id,
      engagement_opportunity_discovery_object.provider_type
    ) |
    engagement_opportunity_tasks.create_engagement_opportunity_task.s(engagement_opportunity_discovery_object) |
    engagement_opportunity_tasks.add_topic_to_engagement_opportunity_task.s(
      engagement_opportunity_discovery_object.topic_type
    )
  ).delay()
