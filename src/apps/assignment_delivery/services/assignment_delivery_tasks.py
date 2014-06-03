from celery import shared_task, chain

from src.aggregates.client.services import client_service, client_tasks
from src.apps.assignment_delivery.services import assignment_delivery_service


@shared_task
def create_and_write_assignments_to_drive_for_clients_task():
  chain(
    client_tasks.create_assignments_for_clients_task.si(),
    write_assignments_to_drive_for_clients_task.si(),
  ).delay()


@shared_task
def write_assignments_to_drive_for_clients_task():
  all_clients = client_service.get_all_clients()
  for client in all_clients:
    write_assignments_to_drive_for_client_task.delay(client.id)


@shared_task
def write_assignments_to_drive_for_client_task(client_id):
  client = client_service.get_client_from_id(client_id)
  return assignment_delivery_service.write_assignments_to_drive_for_client(client)
