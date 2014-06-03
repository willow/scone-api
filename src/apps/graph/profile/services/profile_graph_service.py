from src.apps.graph.profile.services.profile_graph_repository import write_profile_to_graphdb

def create_profile_in_graphdb(profile_uid):
  return write_profile_to_graphdb(profile_uid).properties
