from src.apps.graph.prospect.services.prospect_graph_repository import write_prospect_to_graphdb


def create_prospect_in_graphdb(prospect_uid):
  return write_prospect_to_graphdb(prospect_uid).properties
