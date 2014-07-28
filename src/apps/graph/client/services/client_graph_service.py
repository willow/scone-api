from src.apps.graph.client.services.client_graph_repository import write_client_to_graphdb, \
  write_ta_topic_to_graphdb, delete_client_from_graphdb, delete_ta_topic_from_graphdb


def create_client_in_graphdb(client_uid):
  return write_client_to_graphdb(client_uid).properties


def create_ta_topic_in_graphdb(client_uid, ta_topic_uid, topic_uid):
  return write_ta_topic_to_graphdb(client_uid, ta_topic_uid, topic_uid).properties


def delete_client_in_graphdb(client_uid):
  delete_client_from_graphdb(client_uid)
  return client_uid


def delete_ta_topic_in_graphdb(client_uid, ta_topic_uid):
  delete_ta_topic_from_graphdb(client_uid, ta_topic_uid)
  return ta_topic_uid
