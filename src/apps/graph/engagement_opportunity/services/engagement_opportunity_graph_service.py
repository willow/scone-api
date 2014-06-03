from src.apps.graph.engagement_opportunity.services.engagement_opportunity_graph_repository import \
  write_engagement_opportunity_to_graphdb, write_topic_to_engagement_opportunity_in_graphdb


def create_engagement_opportunity_in_graphdb(engagement_opportunity_uid, profile_uid):
  return write_engagement_opportunity_to_graphdb(engagement_opportunity_uid, profile_uid).properties


def add_topic_to_engagement_opportunity_in_graphdb(engagement_opportunity_uid, engagement_opportunity_topic_uid,
                                                   topic_uid):
  return write_topic_to_engagement_opportunity_in_graphdb(
    engagement_opportunity_uid,
    engagement_opportunity_topic_uid, topic_uid
  ).properties
