from django.dispatch import receiver
from src.aggregates.client.services import client_service
from src.aggregates.engagement_assignment.models import EngagementAssignment
from src.aggregates.engagement_assignment.signals import created
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.apps.graph.engagement_assignment.services import engagement_assignment_graph_tasks


@receiver(created, sender=EngagementAssignment)
def engagement_assignment_created_callback(**kwargs):
  client_id = kwargs.pop('client_id')
  engagement_opportunity_id = kwargs.pop('engagement_opportunity_id')
  
  client_uid = client_service.get_client_from_id(client_id).client_uid
  engagement_opportunity_uid = engagement_opportunity_service.get_engagement_opportunity(
    engagement_opportunity_id
  ).engagement_opportunity_uid
  
  engagement_assignment_graph_tasks.create_engagement_assignment_in_graphdb_task.delay(
    kwargs['instance'].engagement_assignment_uid,
    client_uid,
    engagement_opportunity_uid
  )
