from src.aggregates.engagement_assignment import factories


def save_or_update(engagement_assignment):
  engagement_assignment.save(internal=True)

def create_enagement_assignment(client, engagement_opportunity):
  engagement_assignment = factories.create_engagement_assignment(client, engagement_opportunity)
  save_or_update(engagement_assignment)
  return engagement_assignment
