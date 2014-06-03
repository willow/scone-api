from src.aggregates.engagement_assignment.models import EngagementAssignment


def create_engagement_assignment(client, engagement_opportunity):
  engagement_assignment = EngagementAssignment._from_client_and_engagement_opportunity(
    client,
    engagement_opportunity
  )

  return engagement_assignment
