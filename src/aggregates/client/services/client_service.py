from src.aggregates.client import factories
from src.aggregates.client.models import Client


def save_or_update(client):
  client.save(internal=True)


def create_client(client_name, client_type):
  client = factories.create_client(client_name, client_type)
  save_or_update(client)
  return client


def delete_client(client):
  client.delete(internal=True)


def get_all_clients():
  return Client.objects.all()


def get_enabled_clients():
  return get_all_clients().filter(enabled=True)


def get_client_from_id(client_id):
  return Client.objects.get(id=client_id)
