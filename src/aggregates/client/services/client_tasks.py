from src.aggregates.client.services import client_service
from celery import shared_task

@shared_task
def create_assignments_for_clients_task():
  all_clients = client_service.get_all_clients()
  return client_service.create_assignments_for_clients(all_clients)
