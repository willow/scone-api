from src.aggregates.client.models import Client


def create_client(client_name, client_type):
  client = Client._from_attrs(client_name, client_type)

  return client
