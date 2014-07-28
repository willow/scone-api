from src.apps.graph import constants
from src.libs.graphdb_utils.services import graphdb_provider


def write_engagement_assignment_to_graphdb(engagement_assignment_uid, client_uid,
                                           assignment_attrs, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  params = {

    'client_uid': client_uid,
    'engagement_assignment_uid': engagement_assignment_uid,

  }

  q = '''
    CREATE (ea:EngagementAssignment)
    SET ea.engagement_assignment_uid = { engagement_assignment_uid }
    WITH ea
    MATCH (client:Client)
    WHERE client.client_uid = { client_uid }
    CREATE (client)-[:HAS_ASSIGNMENT]->(ea)
  '''

  if constants.ASSIGNED_EO_UIDS in assignment_attrs:
    q += '''
        FOREACH (eo_param IN { eos } |
          MERGE (eo:EngagementOpportunity {engagement_opportunity_uid: eo_param.engagement_opportunity_uid})
          CREATE (eo)-[:ASSIGNED_TO]->(ea))
    '''

    params['eos'] = [{'engagement_opportunity_uid': eo_uid} for eo_uid in assignment_attrs[constants.ASSIGNED_EO_UIDS]]


  # presumably there will only be a single element in the list, but we are iterating through it
  elif constants.ASSIGNED_PROFILE_UIDS in assignment_attrs:
    q += '''
        FOREACH (profile_uid IN { profiles } |
          MERGE (profile:Profile {profile_uid: profile_uid.profile_uid})
          CREATE (profile)-[:ASSIGNED_TO]->(ea))
    '''

    params['profiles'] = [{'profile_uid': profile_uid} for profile_uid in
                          assignment_attrs[constants.ASSIGNED_PROFILE_UIDS]]

  else:
    raise ValueError('assignment attrs invalid')

  q += '''
    RETURN ea
  '''

  ret_val = gdb.query(q, params=params)
  return ret_val[0][0]


def retrieve_grouped_entities_for_client_from_graphdb(client_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      // start by limit the client and its topics
      MATCH (client:Client)-[rel_client_has_topic:TA_TOPIC]->(topic:Topic)
      WHERE client.client_uid = { client_uid }

      // start query for getting potential profiles
      OPTIONAL MATCH (profile_topic:Profile)-[rel_profile_topic:PROFILE_TOPIC]->(topic),
      	    (profile_topic)-[rel_profile_belongs_to_prospect:BELONGS_TO]->(prospect:Prospect)
      OPTIONAL MATCH (profile_topic)-[profile_ea:ASSIGNED_TO]->(ea:EngagementAssignment)

      // carry over potential profiles (we'll limit them later)
      WITH profile_ea, profile_topic, topic

      // start query for getting potential eos
      OPTIONAL MATCH (engagement_opportunity:EngagementOpportunity)-[rel_eo_topic:ENGAGEMENT_OPPORTUNITY_TOPIC]->(topic),
      		  (engagement_opportunity:EngagementOpportunity)-[rel_eo_belongs_to_profile:BELONGS_TO]-(profile:Profile),
      	    (profile)-[rel_profile_belongs_to_prospect:BELONGS_TO]->(prospect:Prospect)
      OPTIONAL MATCH (engagement_opportunity)-[eo_ea:ASSIGNED_TO]->(ea:EngagementAssignment)

      // carry over potential profiles AND profiles (we'll limit them later)
      // make sure to call distinct because when a prospect has multiple profiles, a row will be returned for each profile
      WITH
        eo_ea,
        profile_ea,
        collect(distinct(engagement_opportunity.engagement_opportunity_uid)) as eos,
        collect(distinct(profile_topic.profile_uid)) as profiles,
        prospect.prospect_uid as prospect

      // do the filtering
      WHERE eo_ea IS NULL
      AND profile_ea IS NULL
      AND prospect IS NOT NULL

      RETURN prospect, eos, profiles
  '''

  params = {

    'client_uid': client_uid,

  }

  query_val = gdb.query(q, params=params, returns=(str, list, list))

  return query_val

def retrieve_assignments_from_topic_type(topic_uid, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MATCH (topic:Topic)
      WHERE topic.topic_uid = { topic_uid }
      OPTIONAL MATCH (ea:EngagementAssignment)<-[:ASSIGNED_TO]-(eo:EngagementOpportunity)-[:ENGAGEMENT_OPPORTUNITY_TOPIC]->(topic)
      OPTIONAL MATCH (ea)<-[:ASSIGNED_TO]-(profile:Profile)-[:PROFILE_TOPIC]->(topic)
      RETURN ea
  '''

  params = {

    'topic_uid': topic_uid,

  }

  query_val = gdb.query(q, params=params)

  return query_val
