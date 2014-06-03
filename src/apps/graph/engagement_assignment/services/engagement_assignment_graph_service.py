from src.apps.graph.engagement_assignment.services.engagement_assignment_graph_repository import \
  write_engagement_assignment_to_graphdb, retrieve_engagement_opportunities_for_client_from_graphdb


def create_engagement_assignment_in_graphdb(engagement_assignment_uid, client_uid, engagement_opportunity_uid):
  return write_engagement_assignment_to_graphdb(
    engagement_assignment_uid,
    client_uid,
    engagement_opportunity_uid
  ).properties

def get_engagement_opportunities_for_client(client_uid):
  engagement_oportunities = retrieve_engagement_opportunities_for_client_from_graphdb(client_uid)
  ret_val = [n[0].properties for n in engagement_oportunities]
  return ret_val
