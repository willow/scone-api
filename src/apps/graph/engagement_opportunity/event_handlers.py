from django.dispatch import receiver
from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.aggregates.engagement_opportunity.signals import created, added_topic
from src.aggregates.profile.services import profile_service
from src.aggregates.topic.services import topic_service
from src.apps.graph.engagement_opportunity.services import engagement_opportunity_graph_tasks


@receiver(created, sender=EngagementOpportunity)
def engagement_opportunity_created_callback(**kwargs):
  profile_id = kwargs.pop('profile_id')
  
  profile_uid = profile_service.get_profile(profile_id).profile_uid
  
  engagement_opportunity_graph_tasks.create_engagement_opportunity_in_graphdb_task.delay(
      kwargs['instance'].engagement_opportunity_uid,
      profile_uid
  )


@receiver(added_topic, sender=EngagementOpportunity)
def topic_added_to_engagement_opportunity_callback(**kwargs):
  engagement_opportunity_topic_uid = kwargs.pop('engagement_opportunity_topic_uid')
  topic_id = kwargs.pop('topic_type_id')

  topic_uid = topic_service.get_topic(topic_id).topic_uid
  
  engagement_opportunity_graph_tasks.add_topic_to_engagement_opportunity_in_graphdb_task.delay(
    kwargs['instance'].engagement_opportunity_uid,
    engagement_opportunity_topic_uid,
    topic_uid
  )
