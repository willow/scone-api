from celery import shared_task

from src.apps.maintenance.database.services import database_maintenance_service


@shared_task
def purge_old_data_task():
  return database_maintenance_service.purge_old_data()
