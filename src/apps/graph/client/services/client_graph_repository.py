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


def delete_client_from_graphdb(client_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = """
    MATCH (client:Client)
    WHERE client.client_uid = { client_uid }
    OPTIONAL MATCH (client)-[ta:TA_TOPIC]-()
    OPTIONAL MATCH (client)<-[assigned:ASSIGNED_TO]-(ea:EngagementAssignment)
    DELETE ta, assigned, ea, client
  """
  client_uid = client_uid

  params = {
    'client_uid': client_uid,
  }

  ret_val = gdb.query(q, params=params)

  return ret_val


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


def delete_ta_topic_from_graphdb(client_uid, ta_topic_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
    MATCH (client:Client)
    WHERE client.client_uid = { client_uid }
    MATCH (client)-[r:TA_TOPIC]->(topic:Topic)
    WHERE r.ta_topic_uid = { ta_topic_uid }
    DELETE r
  '''

  ta_topic_uid = ta_topic_uid

  params = {

    'client_uid': client_uid,
    'ta_topic_uid': ta_topic_uid,
  }

  ret_val = gdb.query(q, params=params, returns=(Relationship,))

  return ret_val
