from src.libs.graphdb_utils.services import graphdb_provider
from neo4jrestclient.client import Node


def write_topic_to_graphdb(topic_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      CREATE (n:Topic) 
      SET n.topic_uid = { topic_uid }
      RETURN n
  '''
  
  params = {
    
    'topic_uid': topic_uid,

  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]


def write_subtopic_to_graphdb(topic_uid, subtopic_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MATCH (topic:Topic)
      WHERE topic.topic_uid = { topic_uid }
      CREATE (subtopic:Subtopic)-[:BELONGS_TO]->(topic)
      SET subtopic.subtopic_uid = { subtopic_uid }
      RETURN topic
  '''
  
  params = {
    
    "topic_uid": topic_uid,
    "subtopic_uid": subtopic_uid,
    
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]
