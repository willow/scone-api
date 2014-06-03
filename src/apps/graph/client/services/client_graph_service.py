from src.apps.graph.client.services.client_graph_repository import write_client_to_graphdb, write_ta_topic_to_graphdb


def create_client_in_graphdb(client_uid):
  return write_client_to_graphdb(client_uid).properties


def create_ta_topic_in_graphdb(client_uid, ta_topic_uid, topic_uid):
  return write_ta_topic_to_graphdb(client_uid, ta_topic_uid, topic_uid).properties
