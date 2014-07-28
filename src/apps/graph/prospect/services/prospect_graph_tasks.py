from celery import shared_task
from src.apps.graph.prospect.services import prospect_graph_service


@shared_task
def create_prospect_in_graphdb_task(prospect_uid):
  return prospect_graph_service.create_prospect_in_graphdb(prospect_uid)['prospect_uid']
