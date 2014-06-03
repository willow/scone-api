from src.aggregates.engagement_opportunity.models import EngagementOpportunity


def construct_engagement_opportunity_from_discovery(profile, engagement_opportunity_discovery_object):
  engagement_opportunity = EngagementOpportunity._from_engagement_discovery(
    profile.id, engagement_opportunity_discovery_object
  )
  return engagement_opportunity
