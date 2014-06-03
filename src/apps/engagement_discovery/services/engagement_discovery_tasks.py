from celery import shared_task
from src.apps.engagement_discovery.services import engagement_discovery_service


@shared_task
def discover_engagement_opportunities_task():
  return engagement_discovery_service.discover_engagement_opportunities()
