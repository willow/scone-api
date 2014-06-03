from src.libs.graphdb_utils.services import graphdb_provider
from neo4jrestclient.client import Node, Relationship


def write_client_to_graphdb(client_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = "CREATE (n:Client { props }) RETURN n"
  client_uid = client_uid
  params = {
    'props': 
      {
        'client_uid': client_uid,
      }
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  
  return ret_val[0][0]

def write_ta_topic_to_graphdb(client_uid, ta_topic_uid, topic_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()
  
  q = '''
    MATCH (client:Client), (topic:Topic)
    WHERE client.client_uid = { client_uid }
    AND topic.topic_uid = { topic_uid }
    CREATE (client)-[r:TA_TOPIC]->(topic)
    SET r.ta_topic_uid = { ta_topic_uid } 
    RETURN r
  '''
  
  ta_topic_uid = ta_topic_uid
  topic_uid = topic_uid
  params = {
    
    'client_uid': client_uid,
    'ta_topic_uid': ta_topic_uid,
    'topic_uid': topic_uid,
    
  }

  ret_val = gdb.query(q, params=params, returns=(Relationship,))
  
  return ret_val[0][0]
