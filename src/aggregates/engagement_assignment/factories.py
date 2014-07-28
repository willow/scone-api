from src.aggregates.engagement_assignment.models import EngagementAssignment


def create_engagement_assignment(client, assignment_attrs):
  engagement_assignment = EngagementAssignment._from_client_and_engagement_opportunity(
    client,
    assignment_attrs
  )

  return engagement_assignment
