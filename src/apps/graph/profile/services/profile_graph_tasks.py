from celery import shared_task
from src.apps.graph.profile.services import profile_graph_service

@shared_task
def create_profile_in_graphdb_task(profile_uid):
  return profile_graph_service.create_profile_in_graphdb(profile_uid)['profile_uid']
