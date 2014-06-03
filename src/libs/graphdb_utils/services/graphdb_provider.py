from neo4jrestclient.client import GraphDatabase
from django.conf import settings


def get_graph_client():
  return GraphDatabase(settings.GRAPH_DB_URL, settings.GRAPH_DB_USERNAME, settings.GRAPH_DB_PASSWORD)
