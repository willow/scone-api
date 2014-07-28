from neo4jrestclient.client import Node
from src.apps.graph import constants
from src.libs.graphdb_utils.services import graphdb_provider


def write_profile_to_graphdb(profile_uid, prospect_uid, _graph_db_provider=graphdb_provider, **kwargs):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
        MATCH (prospect:Prospect)
        WHERE prospect.prospect_uid = { prospect_uid }
        CREATE (profile:Profile)
        SET profile.profile_uid = { profile_uid }
        CREATE (profile)-[:BELONGS_TO]->(prospect)
    '''
  params = {
    'profile_uid': profile_uid,
    'prospect_uid': prospect_uid,
  }

  if constants.TOPIC_UIDS in kwargs:
    q += '''
          FOREACH (topic_param IN { topics } |
            MERGE (topic:Topic {topic_uid: topic_param.topic_uid})
            CREATE (profile)-[:PROFILE_TOPIC]->(topic))
      '''

    params['topics'] = [{'topic_uid': topic_uid} for topic_uid in kwargs[constants.TOPIC_UIDS]]
  q += '''
        RETURN profile
  '''

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]
