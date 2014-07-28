from django.core.management.base import NoArgsCommand
from src.aggregates.engagement_assignment.services import engagement_assignment_tasks


class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    engagement_assignment_tasks.refresh_assignments_for_clients_task.delay()
