from src.aggregates.client import factories
from src.aggregates.client.models import Client
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.apps.graph.engagement_assignment.services import engagement_assignment_graph_service


def save_or_update(client):
  client.save(internal=True)


def create_client(client_name, client_type):
  client = factories.create_client(client_name, client_type)
  save_or_update(client)
  return client


def get_all_clients():
  return Client.objects.all()


def create_assignments_for_clients(clients):
  for client in clients:
    eo_to_add = engagement_assignment_graph_service.get_engagement_opportunities_for_client(client.client_uid)
    for eo in eo_to_add:
      eo_entity = engagement_opportunity_service.get_engagement_opportunity_from_uid(eo['engagement_opportunity_uid'])
      client.assign_engagement_opportunity(eo_entity.id)
    save_or_update(client)


def get_client_from_id(client_id):
  return Client.objects.get(id=client_id)
