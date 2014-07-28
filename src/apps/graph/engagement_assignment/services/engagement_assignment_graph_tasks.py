from celery import shared_task
from src.apps.graph.engagement_assignment.services import engagement_assignment_graph_service
import logging
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def create_engagement_assignment_in_graphdb_task(self, engagement_assignment_uid, client_uid, assignment_attrs):
  log_message = (
    "Create ea in graph db. ea_uid: %s, client_uid: %s, assignment_attrs: %s",
    engagement_assignment_uid, client_uid, assignment_attrs
  )

  try:
    with log_wrapper(logger.debug, *log_message):

      ret_val = engagement_assignment_graph_service.create_engagement_assignment_in_graphdb(
        engagement_assignment_uid,
        client_uid,
        assignment_attrs
      )['engagement_assignment_uid']

    return ret_val
  except Exception as e:
    self.retry(exc=e)


@shared_task
def get_engagement_opportunities_for_client(client_uid):
  return engagement_assignment_graph_service.get_grouped_entities_for_client(client_uid)
