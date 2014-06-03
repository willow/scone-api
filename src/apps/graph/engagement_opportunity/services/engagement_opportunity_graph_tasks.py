from celery import shared_task
from src.apps.graph.engagement_opportunity.services import engagement_opportunity_graph_service


@shared_task
def create_engagement_opportunity_in_graphdb_task(engagement_opportunity_uid, profile_uid):
  return engagement_opportunity_graph_service.create_engagement_opportunity_in_graphdb(
    engagement_opportunity_uid,
    profile_uid
  )['engagement_opportunity_uid']


@shared_task
def add_topic_to_engagement_opportunity_in_graphdb_task(engagement_opportunity_uid, engagement_opportunity_topic_uid,
                                                        topic_uid):
  return engagement_opportunity_graph_service.add_topic_to_engagement_opportunity_in_graphdb(
    engagement_opportunity_uid,
    engagement_opportunity_topic_uid,
    topic_uid
  )['engagement_opportunity_topic_uid']
