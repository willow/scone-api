from src.aggregates.engagement_assignment.signals import delivered
from django.dispatch import receiver
from src.apps.domain.engagement_assignment.services import assigned_prospect_tasks


@receiver(delivered)
def profile_created_callback(**kwargs):
  ea_uid = kwargs['engagement_assignment_uid']
  system_created_date = kwargs['system_created_date']
  assigned_prospect_tasks.update_assigned_prospect_task.delay(ea_uid, system_created_date)
