from neo4jrestclient.client import Node
from src.libs.graphdb_utils.services import graphdb_provider


def write_prospect_to_graphdb(prospect_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''CREATE (n:Prospect { props }) RETURN n'''
  params = {
    'props':
      {
        'prospect_uid': prospect_uid,
      }
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]
