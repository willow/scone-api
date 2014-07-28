from src.aggregates.prospect.services import prospect_tasks
from django.dispatch import receiver
from src.aggregates.profile.signals import created


@receiver(created)
def profile_created_callback(**kwargs):
  prospect_id = kwargs['prospect_id']
  prospect_tasks.manage_prospect_profiles_task.delay(prospect_id)
