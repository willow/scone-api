from celery import shared_task, chain, chord

from src.aggregates.client.services import client_service
from src.aggregates.engagement_assignment.services import engagement_assignment_tasks, engagement_assignment_service
from src.apps.assignment_delivery.services import assignment_delivery_service


@shared_task
def create_and_deliver_assignments_to_drive_for_clients_task():
  chord(
    engagement_assignment_tasks.get_refresh_assignments_for_clients_group(),
    deliver_assignments_to_drive_for_clients_task.si(),
  ).delay()


@shared_task
def deliver_assignments_to_drive_for_clients_task():
  all_clients = client_service.get_enabled_clients()
  for client in all_clients:
    chain(
      get_new_client_assignments_task.si(client.id),
      # prepare_assignments_for_delivery should actually probably be a group (celery) - that way each ea is its own
      # task. Ex: http://stackoverflow.com/a/14995090/173957
      prepare_assignments_for_delivery_task.s(),
      write_assignments_to_drive_task.s(client.id)
    ).delay()


@shared_task
def get_new_client_assignments_task(client_id):
  client = client_service.get_client_from_id(client_id)
  return list(assignment_delivery_service.get_new_client_assignments_ids(client))


@shared_task
def prepare_assignments_for_delivery_task(assignment_ids):
  for aid in assignment_ids:
    ea = engagement_assignment_service.get_engagement_assignment(aid)
    assignment_delivery_service.prepare_assignment_for_delivery(ea)

  return assignment_ids


@shared_task
def write_assignments_to_drive_task(assignment_ids, client_id):
  client = client_service.get_client_from_id(client_id)
  assignments = engagement_assignment_service.get_engagement_assignments_by_score(assignment_ids)
  return assignment_delivery_service.write_assignments_to_drive(assignments, client)
