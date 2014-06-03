from celery import shared_task

from src.aggregates.client.services.client_service import get_client_from_id
from src.aggregates.engagement_assignment.services import engagement_assignment_service
from src.aggregates.engagement_opportunity.services.engagement_opportunity_service import \
  get_engagement_opportunity_from_id


@shared_task
def create_engagement_assignment_task(client_id, engagement_opportunity_id):
  client = get_client_from_id(client_id)
  engagement_opportunity = get_engagement_opportunity_from_id(engagement_opportunity_id)
  return engagement_assignment_service.create_enagement_assignment(client, engagement_opportunity).id
