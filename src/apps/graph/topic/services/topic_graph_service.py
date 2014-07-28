from src.apps.graph.topic.services.topic_graph_repository import write_topic_to_graphdb, write_subtopic_to_graphdb, \
  delete_topic_from_graphdb, delete_subtopic_from_graphdb


def create_topic_in_graphdb(topic_uid):
  return write_topic_to_graphdb(topic_uid).properties


def create_subtopic_in_graphdb(topic_uid, subtopic_uid):
  return write_subtopic_to_graphdb(topic_uid, subtopic_uid).properties


def delete_topic_in_graphdb(topic_uid):
  delete_topic_from_graphdb(topic_uid)
  return topic_uid


def delete_subtopic_in_graphdb(topic_uid, subtopic_uid):
  delete_subtopic_from_graphdb(topic_uid, subtopic_uid)
  return subtopic_uid
