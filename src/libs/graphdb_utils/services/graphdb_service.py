from neo4jrestclient.client import GraphDatabase
from django.conf import settings


def purge_data(graph_client):
  graph_client.query("""MATCH (n)
      OPTIONAL MATCH (n)-[r]-()
      DELETE n,r""")
