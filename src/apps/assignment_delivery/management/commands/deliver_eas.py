from django.core.management.base import NoArgsCommand
from src.apps.assignment_delivery.services.assignment_delivery_tasks import \
  create_and_deliver_assignments_to_drive_for_clients_task


class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    create_and_deliver_assignments_to_drive_for_clients_task.delay()
