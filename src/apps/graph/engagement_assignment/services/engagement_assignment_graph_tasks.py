from celery import shared_task
from src.apps.graph.engagement_assignment.services import engagement_assignment_graph_service


@shared_task
def create_engagement_assignment_in_graphdb_task(engagement_assignment_uid, client_uid, engagement_opportunity_uid):
  return engagement_assignment_graph_service.create_engagement_assignment_in_graphdb(
    engagement_assignment_uid,
    client_uid,
    engagement_opportunity_uid
  )['engagement_assignment_uid']

@shared_task
def get_engagement_opportunities_for_client(client_uid):
  return engagement_assignment_graph_service.get_engagement_opportunities_for_client(client_uid)
