from src.apps.graph.engagement_assignment.services.engagement_assignment_graph_repository import \
  write_engagement_assignment_to_graphdb, \
  retrieve_assignments_from_topic_type, \
  retrieve_grouped_entities_for_client_from_graphdb


def create_engagement_assignment_in_graphdb(engagement_assignment_uid, client_uid, assignment_attrs):
  return write_engagement_assignment_to_graphdb(
    engagement_assignment_uid,
    client_uid,
    assignment_attrs
  )['data']


def get_grouped_entities_for_client(client_uid):
  ret_val = []

  query_val = retrieve_grouped_entities_for_client_from_graphdb(client_uid)

  for row in query_val:
    ret_val.append({'prospect_uid': row[0], 'eo_uids': row[1], 'profile_uids': row[2]})

  return ret_val


def get_assignments_from_topic_type(topic_uid):
  ret_val = retrieve_assignments_from_topic_type(topic_uid)

  if ret_val:
    ret_val = [x[0]['data']['engagement_assignment_uid'] for x in ret_val]
  else:
    ret_val = []

  return ret_val
