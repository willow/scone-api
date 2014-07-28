from src.aggregates.engagement_assignment.services import engagement_assignment_service
from src.aggregates.client.services import client_service
from celery import shared_task, group
import logging
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@shared_task
def refresh_assignments_for_clients_task():
  group = get_refresh_assignments_for_clients_group()
  group.delay()


def get_refresh_assignments_for_clients_group():
  all_clients = client_service.get_enabled_clients()

  ret_val = group(refresh_assignments_for_client_task.si(client.id) for client in all_clients)

  return ret_val


@shared_task
def refresh_assignments_for_client_task(client_id):
  log_message = (
    "Refresh assignments task for client_id: %s",
    client_id
  )

  with log_wrapper(logger.debug, *log_message):
    client = client_service.get_client_from_id(client_id)

    ret_val = engagement_assignment_service.refresh_assignments(client)

  return ret_val
