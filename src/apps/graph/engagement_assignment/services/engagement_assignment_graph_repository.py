from src.libs.graphdb_utils.services import graphdb_provider
from neo4jrestclient.client import Relationship, Node

def write_engagement_assignment_to_graphdb(engagement_assignment_uid, client_uid, 
                                           engagement_opportunity_uid, _graph_db_provider=graphdb_provider):
  
  gdb = _graph_db_provider.get_graph_client()

  engagement_assignment_uid = engagement_assignment_uid
  client_uid = client_uid
  engagement_opportunity_uid = engagement_opportunity_uid

  q = '''
      MATCH (client:Client), (engagement_opportunity:EngagementOpportunity)
      WHERE client.client_uid = { client_uid }
      AND engagement_opportunity.engagement_opportunity_uid = { engagement_opportunity_uid }
      CREATE (client)-[r:ENGAGEMENT_ASSIGNMENT]->(engagement_opportunity)
      SET r.engagement_assignment_uid = { engagement_assignment_uid }
      RETURN r
  '''

  params = {

    'client_uid': client_uid,
    'engagement_opportunity_uid': engagement_opportunity_uid,
    'engagement_assignment_uid': engagement_assignment_uid,

  }

  ret_val = gdb.query(q, params=params, returns=(Relationship,))
  return ret_val[0][0]

def retrieve_engagement_opportunities_for_client_from_graphdb(client_uid, _graph_db_provider=graphdb_provider):
  
  gdb = _graph_db_provider.get_graph_client()
  
  client_uid = client_uid
  
  q = '''
      MATCH (client:Client)-[:TA_TOPIC]->(topic)
      MATCH (engagement_opportunity:EngagementOpportunity)-[:ENGAGEMENT_OPPORTUNITY_TOPIC]->(topic)
      WHERE client.client_uid = { client_uid }
      AND NOT (client)-[:ENGAGEMENT_ASSIGNMENT]->(engagement_opportunity)
      RETURN engagement_opportunity
  '''
  
  params = {
    
    'client_uid': client_uid,
    
  }
  
  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val
