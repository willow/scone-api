from neo4jrestclient.client import Node, Relationship
from src.libs.graphdb_utils.services import graphdb_provider


def write_engagement_opportunity_to_graphdb(engagement_opportunity_uid, profile_uid, 
  _graph_db_provider=graphdb_provider):
  
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MATCH (profile:Profile)
      WHERE profile.profile_uid = { profile_uid }
      CREATE (engagement_opportunity:EngagementOpportunity)
      SET engagement_opportunity.engagement_opportunity_uid = { engagement_opportunity_uid }
      CREATE (engagement_opportunity)-[:BELONGS_TO]->(profile)
      RETURN engagement_opportunity
  '''
  engagement_opportunity_uid = engagement_opportunity_uid
  profile_uid = profile_uid
  params = {
    
    'profile_uid': profile_uid,
    'engagement_opportunity_uid': engagement_opportunity_uid
    
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]


def write_topic_to_engagement_opportunity_in_graphdb(engagement_opportunity_uid, engagement_opportunity_topic_uid,
                                                     topic_uid,
                                                     _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()
  
  q = '''
      MATCH (topic:Topic), (engagement_opportunity:EngagementOpportunity)
      WHERE topic.topic_uid = { topic_uid }
      AND engagement_opportunity.engagement_opportunity_uid = { engagement_opportunity_uid }
      CREATE (engagement_opportunity)-[r:ENGAGEMENT_OPPORTUNITY_TOPIC]->(topic)
      SET r.engagement_opportunity_topic_uid = { engagement_opportunity_topic_uid }
      RETURN r
  '''
  engagement_opportunity_uid = engagement_opportunity_uid
  engagement_opportunity_topic_uid = engagement_opportunity_topic_uid
  topic_uid = topic_uid
  
  params = {
    
    'engagement_opportunity_uid': engagement_opportunity_uid,
    'engagement_opportunity_topic_uid': engagement_opportunity_topic_uid,
    'topic_uid': topic_uid,
    
  }
  
  ret_val = gdb.query(q, params=params, returns=(Relationship,))
  return ret_val[0][0]
