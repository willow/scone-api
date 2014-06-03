from src.apps.graph.topic.services.topic_graph_repository import write_topic_to_graphdb, write_subtopic_to_graphdb


def create_topic_in_graphdb(topic_uid):
  return write_topic_to_graphdb(topic_uid).properties


def create_subtopic_in_graphdb(topic_uid, subtopic_uid):
  return write_subtopic_to_graphdb(topic_uid, subtopic_uid).properties
